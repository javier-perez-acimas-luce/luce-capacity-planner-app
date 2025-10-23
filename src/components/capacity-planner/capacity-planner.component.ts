import { ChangeDetectionStrategy, Component, computed, inject, signal, OnInit, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BigQueryService, Project, TeamMember, Assignment, ProjectCase } from '../../services/bigquery.service';
import { forkJoin } from 'rxjs';

export interface ProjectCapacity {
  id: number;
  name: string;
  group: string;
  projectCase: { [key: string]: number };
  assignments: { [key: string]: number };
}

@Component({
  selector: 'app-capacity-planner',
  imports: [CommonModule],
  templateUrl: './capacity-planner.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CapacityPlannerComponent implements OnInit {
  private bigQueryService = inject(BigQueryService);
  
  loading = signal<boolean>(true);

  // Static data signals
  sprints = signal<string[]>([]);
  projectGroups = signal<string[]>([]);
  teams = signal<string[]>([]);
  projects = signal<Project[]>([]);
  teamMembers = signal<TeamMember[]>([]);
  
  // Dynamic data signals
  assignments = signal<Assignment[]>([]);
  projectCases = signal<ProjectCase[]>([]);

  // Filter signals
  selectedSprints = signal<string[]>([]);
  selectedGroup = signal<string>('All Groups');
  selectedTeam = signal<string>('All Teams');
  projectNameFilter = signal<string>('');

  constructor() {
    effect(() => {
        const sprints = this.selectedSprints();
        if (sprints.length > 0) {
            this.loading.set(true);
            this.bigQueryService.getSprintData(sprints).subscribe(data => {
                this.assignments.set(data.assignments);
                this.projectCases.set(data.projectCases);
                this.loading.set(false);
            });
        } else {
            this.assignments.set([]);
            this.projectCases.set([]);
        }
    }, { allowSignalWrites: true });
  }

  projectsGroupedBySprint = computed(() => {
    const sprints = this.selectedSprints();
    const allProjects = this.projects();
    const allAssignments = this.assignments();
    const allProjectCases = this.projectCases();
    const group = this.selectedGroup();
    const nameFilter = this.projectNameFilter().toLowerCase();

    return sprints.map(sprintName => {
        const sprintAssignments = allAssignments.filter(a => a.sprint === sprintName);
        const sprintProjectCases = allProjectCases.filter(pc => pc.sprint === sprintName);

        const projectsForSprint: ProjectCapacity[] = allProjects.map(project => {
            const assignmentsForProject = sprintAssignments.filter(a => a.projectId === project.id);
            const casesForProject = sprintProjectCases.filter(pc => pc.projectId === project.id);

            return {
                ...project,
                assignments: assignmentsForProject.reduce((acc, curr) => {
                    acc[curr.memberId] = curr.days;
                    return acc;
                }, {} as {[memberId: string]: number}),
                projectCase: casesForProject.reduce((acc, curr) => {
                    acc[curr.subteam] = curr.days;
                    return acc;
                }, {} as {[subteam: string]: number}),
            };
        });

        const groupFiltered = group === 'All Groups' ? projectsForSprint : projectsForSprint.filter(p => p.group === group);
        const nameFiltered = nameFilter
            ? groupFiltered.filter(p => p.name.toLowerCase().includes(nameFilter))
            : groupFiltered;

        return { sprint: sprintName, projects: nameFiltered };
    }).filter(group => group.projects.length > 0);
  });

  flatFilteredProjects = computed(() => {
    return this.projectsGroupedBySprint().flatMap(group => group.projects);
  });
  
  allTeams = computed(() => {
    const members = this.teamMembers();
    return [...new Set(members.map(m => m.team))].sort();
  });

  subteamsByTeam = computed(() => {
    const members = this.teamMembers();
    const mapping: { [key: string]: string[] } = {};
    for (const member of members) {
      if (!mapping[member.team]) {
        mapping[member.team] = [];
      }
      if (!mapping[member.team].includes(member.subteam)) {
        mapping[member.team].push(member.subteam);
      }
    }
    for (const team in mapping) {
        mapping[team].sort();
    }
    return mapping;
  });
  
  allSubteams = computed(() => {
    return this.teamMembers().map(m => m.subteam).filter((v, i, a) => a.indexOf(v) === i).sort();
  });

  filteredTeamMembers = computed(() => {
    const team = this.selectedTeam();
    const allMembers = this.teamMembers();
    if (team === 'All Teams') {
      return allMembers;
    }
    return allMembers.filter(m => m.team === team);
  });
  
  filteredTeams = computed(() => {
     const members = this.filteredTeamMembers();
     return [...new Set(members.map(m => m.team))].sort();
  });

  membersByTeam = computed(() => {
    const teams = this.allTeams();
    const members = this.filteredTeamMembers();
    const mapping: {[key: string]: TeamMember[]} = {};
    for(const team of teams) {
        mapping[team] = members.filter(m => m.team === team);
    }
    return mapping;
  });

  totalColumns = computed(() => {
    return 2 + this.allSubteams().length + 1 + this.filteredTeamMembers().length + this.filteredTeams().length + this.filteredTeams().length + 1;
  });

  // --- Calculation Signals ---
  
  totalAssignedPerMember = computed(() => {
    const totals: { [key: string]: number } = {};
    this.teamMembers().forEach(member => {
      totals[member.id] = this.flatFilteredProjects().reduce((acc, project) => {
        return acc + (project.assignments[member.id] || 0);
      }, 0);
    });
    return totals;
  });

  differencePerMember = computed(() => {
    const diffs: { [key: string]: number } = {};
    const assigned = this.totalAssignedPerMember();
    this.teamMembers().forEach(member => {
      diffs[member.id] = member.expectedDays - assigned[member.id];
    });
    return diffs;
  });

  totalAssignedPerProject(project: ProjectCapacity): number {
    return Object.values(project.assignments).reduce((sum, days) => sum + days, 0);
  }
  
  totalExpectedPerProjectCase(project: ProjectCapacity): number {
    return Object.values(project.projectCase).reduce((sum, days) => sum + (days || 0), 0);
  }

  totalAssignedPerTeamForProject(project: ProjectCapacity, team: string): number {
      const membersInTeam = this.teamMembers().filter(m => m.team === team);
      return membersInTeam.reduce((sum, member) => {
          return sum + (project.assignments[member.id] || 0);
      }, 0);
  }

  totalExpectedPerTeamForProject(project: ProjectCapacity, team: string): number {
    const subteams = this.subteamsByTeam()[team] || [];
    return subteams.reduce((sum, subteam) => sum + (project.projectCase[subteam] || 0), 0);
  }

  differencePerTeamForProject(project: ProjectCapacity, team: string): number {
    const assigned = this.totalAssignedPerTeamForProject(project, team);
    const expected = this.totalExpectedPerTeamForProject(project, team);
    return assigned - expected;
  }
  
  grandTotalAssignedPerTeam = computed(() => {
      const totals: { [key: string]: number } = {};
      const assignedPerMember = this.totalAssignedPerMember();
      const teams = this.allTeams();
      const members = this.teamMembers();

      for (const team of teams) {
          totals[team] = members
              .filter(m => m.team === team)
              .reduce((sum, member) => sum + (assignedPerMember[member.id] || 0), 0);
      }
      return totals;
  });
  
  grandTotalAssigned = computed(() => {
      return Object.values(this.grandTotalAssignedPerTeam()).reduce((sum: number, days) => sum + Number(days), 0);
  });
  
  totalExpectedFromCasePerSubteam = computed(() => {
      const totals: { [key: string]: number } = {};
      const projects = this.flatFilteredProjects();
      const subteams = this.allSubteams();

      for (const subteam of subteams) {
          totals[subteam] = projects.reduce((acc, project) => acc + (project.projectCase[subteam] || 0), 0);
      }
      return totals;
  });
  
  grandTotalExpectedFromCase = computed(() => {
      const subteamTotals = this.totalExpectedFromCasePerSubteam();
      return Object.values(subteamTotals).reduce((sum: number, days) => sum + Number(days), 0);
  });
  
  ngOnInit(): void {
    this.loading.set(true);
    forkJoin({
        sprints: this.bigQueryService.getSprints(),
        projectData: this.bigQueryService.getProjectsAndGroups(),
        teamData: this.bigQueryService.getTeamData(),
    }).subscribe(({ sprints, projectData, teamData }) => {
        this.sprints.set(sprints);
        this.projects.set(projectData.projects);
        this.projectGroups.set(projectData.projectGroups);
        this.teamMembers.set(teamData.teamMembers);
        this.teams.set(teamData.teams);
        
        const firstSprint = sprints[0];
        if (firstSprint) {
            this.selectedSprints.set([firstSprint]);
        } else {
            this.loading.set(false);
        }
    });
  }

  onGroupChange(event: Event): void {
    this.selectedGroup.set((event.target as HTMLSelectElement).value);
  }

  onProjectNameChange(event: Event): void {
    this.projectNameFilter.set((event.target as HTMLInputElement).value);
  }
  
  onSprintChange(event: Event): void {
    const selectedOptions = (event.target as HTMLSelectElement).selectedOptions;
    const selectedValues = Array.from(selectedOptions).map(option => option.value);
    this.selectedSprints.set(selectedValues);
  }
  
  onTeamChange(event: Event): void {
    this.selectedTeam.set((event.target as HTMLSelectElement).value);
  }

  updateDays(sprint: string, projectId: number, memberId: string, event: Event): void {
    const inputElement = event.target as HTMLInputElement;
    const days = parseInt(inputElement.value, 10) || 0;

    this.assignments.update(current => {
        const index = current.findIndex(a => a.sprint === sprint && a.projectId === projectId && a.memberId === memberId);
        if (index > -1) {
            const newAssignments = [...current];
            newAssignments[index] = { ...newAssignments[index], days };
            return newAssignments;
        }
        return [...current, { sprint, projectId, memberId, days }];
    });

    this.bigQueryService.updateAssignment({ sprint, projectId, memberId, days })
        .subscribe({ error: (err) => console.error('Failed to update assignment', err) });
  }

  updateProjectCase(sprint: string, projectId: number, subteam: string, event: Event): void {
    const inputElement = event.target as HTMLInputElement;
    const days = parseInt(inputElement.value, 10) || 0;

    this.projectCases.update(current => {
        const index = current.findIndex(pc => pc.sprint === sprint && pc.projectId === projectId && pc.subteam === subteam);
        if (index > -1) {
            const newCases = [...current];
            newCases[index] = { ...newCases[index], days };
            return newCases;
        }
        return [...current, { sprint, projectId, subteam, days }];
    });

    this.bigQueryService.updateProjectCase({ sprint, projectId, subteam, days })
        .subscribe({ error: (err) => console.error('Failed to update project case', err) });
  }
  
  trackById(index: number, item: any): any {
    return item.id;
  }
  
  trackByName(index: number, item: string): string {
    return item;
  }
}
