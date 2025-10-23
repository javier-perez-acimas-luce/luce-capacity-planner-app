
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-power-bi-dashboard',
  templateUrl: './power-bi-dashboard.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PowerBiDashboardComponent {
  private sanitizer = inject(DomSanitizer);

  // IMPORTANT: Replace this with your actual Power BI embed URL
  powerBiUrl: SafeResourceUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
    'https://app.powerbi.com/reportEmbed?reportId=your-report-id&autoAuth=true&ctid=your-tenant-id'
  );
}
