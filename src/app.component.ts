
import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { CapacityPlannerComponent } from './components/capacity-planner/capacity-planner.component';
import { PowerBiDashboardComponent } from './components/power-bi-dashboard/power-bi-dashboard.component';

type View = 'planner' | 'dashboard';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CapacityPlannerComponent, PowerBiDashboardComponent],
})
export class AppComponent {
  activeView = signal<View>('planner');

  setView(view: View): void {
    this.activeView.set(view);
  }
}
