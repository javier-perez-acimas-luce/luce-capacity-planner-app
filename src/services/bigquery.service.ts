import { Injectable } from '@angular/core';
import { Observable, of, delay, forkJoin } from 'rxjs';

// Data models reflecting BigQuery table structures
export interface TeamMember {
  id: string;
  name: string;
  team: string;
  subteam: string;
  expectedDays: number;
}

export interface Project {
  id: number;
  name: string;
  group: string;
}

export interface Assignment {
  sprint: string;
  projectId: number;
  memberId: string;
  days: number;
}

export interface ProjectCase {
  sprint: string;
  projectId: number;
  subteam: string;
  days: number;
}

@Injectable({
  providedIn: 'root',
})
export class BigQueryService {
  // Mock data that would come from BigQuery tables
  private mockSprints = ['Sprint 2024.10', 'Sprint 2024.11', 'Sprint 2024.12'];
  private mockProjectGroups = ['All Groups', 'Core Platform', 'Growth Initiatives', 'Internal Tools'];
  private mockTeams = ['All Teams', 'DATA', 'DEVELOP', 'ANALYTIC', 'IT'];
  
  private mockProjects: Project[] = [
    { id: 1, name: 'Phoenix Project', group: 'Core Platform' },
    { id: 2, name: 'Project Chimera', group: 'Growth Initiatives' },
    { id: 3, name: 'Odyssey Initiative', group: 'Core Platform' },
    { id: 4, name: 'Quantum Leap', group: 'Internal Tools' },
  ];
  
  private mockTeamMembers: TeamMember[] = [
    { id: 'alice', name: 'Alice', team: 'DATA', subteam: 'Data Engineer', expectedDays: 18 },
    { id: 'bob', name: 'Bob', team: 'DATA', subteam: 'BI', expectedDays: 20 },
    { id: 'charlie', name: 'Charlie', team: 'DEVELOP', subteam: 'Backend', expectedDays: 20 },
    { id: 'diana', name: 'Diana', team: 'DEVELOP', subteam: 'Frontend', expectedDays: 15 },
    { id: 'grace', name: 'Grace', team: 'DEVELOP', subteam: 'Mobile', expectedDays: 17 },
    { id: 'ethan', name: 'Ethan', team: 'IT', subteam: 'Cloud', expectedDays: 22 },
    { id: 'frank', name: 'Frank', team: 'ANALYTIC', subteam: 'Analyst', expectedDays: 19 },
  ];

  // This simulates the 'assignations' table, keyed by sprint
  private mockAssignments: Assignment[] = [];

  // This simulates the 'project_case' table, also keyed by sprint
  private mockProjectCases: ProjectCase[] = [];

  constructor() {
    this.prepopulateMockData();
  }
  
  private prepopulateMockData(): void {
      this.mockSprints.forEach(sprint => {
          this.mockProjects.forEach(project => {
              this.mockTeamMembers.forEach(member => {
                  this.mockAssignments.push({ sprint, projectId: project.id, memberId: member.id, days: 0 });
              });
              
              if(project.id === 1) { // Phoenix Project
                  this.mockProjectCases.push({ sprint, projectId: 1, subteam: 'Data Engineer', days: 5 });
                  this.mockProjectCases.push({ sprint, projectId: 1, subteam: 'BI', days: 5 });
                  this.mockProjectCases.push({ sprint, projectId: 1, subteam: 'Backend', days: 15 });
                  this.mockProjectCases.push({ sprint, projectId: 1, subteam: 'Frontend', days: 10 });
                  this.mockProjectCases.push({ sprint, projectId: 1, subteam: 'Cloud', days: 5 });
              }
               if(project.id === 2) { // Project Chimera
                  this.mockProjectCases.push({ sprint, projectId: 2, subteam: 'Data Engineer', days: 10 });
                  this.mockProjectCases.push({ sprint, projectId: 2, subteam: 'BI', days: 5 });
                  this.mockProjectCases.push({ sprint, projectId: 2, subteam: 'Backend', days: 20 });
               }
          });
      });
  }

  getSprints(): Observable<string[]> {
    return of(this.mockSprints).pipe(delay(200));
  }

  getProjectsAndGroups(): Observable<{ projects: Project[], projectGroups: string[] }> {
    return of({
      projects: this.mockProjects,
      projectGroups: this.mockProjectGroups
    }).pipe(delay(300));
  }
  
  getTeamData(): Observable<{ teamMembers: TeamMember[], teams: string[] }> {
    return of({
      teamMembers: this.mockTeamMembers,
      teams: this.mockTeams,
    }).pipe(delay(400));
  }
  
  // Fetch assignments and project cases for a given list of sprints
  getSprintData(sprints: string[]): Observable<{ assignments: Assignment[], projectCases: ProjectCase[] }> {
      const assignments = this.mockAssignments.filter(a => sprints.includes(a.sprint));
      const projectCases = this.mockProjectCases.filter(pc => sprints.includes(pc.sprint));
      return of({ assignments, projectCases }).pipe(delay(500));
  }

  // Update a single assignment
  updateAssignment(assignment: Assignment): Observable<Assignment> {
    const index = this.mockAssignments.findIndex(a => 
      a.sprint === assignment.sprint && 
      a.projectId === assignment.projectId && 
      a.memberId === assignment.memberId
    );
    if (index > -1) {
      this.mockAssignments[index] = assignment;
    } else {
      this.mockAssignments.push(assignment);
    }
    return of(assignment).pipe(delay(150)); // Simulate API response
  }

  // Update a single project case
  updateProjectCase(projectCase: ProjectCase): Observable<ProjectCase> {
    const index = this.mockProjectCases.findIndex(pc => 
      pc.sprint === projectCase.sprint &&
      pc.projectId === projectCase.projectId &&
      pc.subteam === projectCase.subteam
    );
    if (index > -1) {
      this.mockProjectCases[index] = projectCase;
    } else {
      this.mockProjectCases.push(projectCase);
    }
    return of(projectCase).pipe(delay(150));
  }
}
