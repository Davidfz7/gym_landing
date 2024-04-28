import { Component } from '@angular/core';
import Chart from 'chart.js/auto';

@Component({
  selector: 'app-admin-report',
  standalone: true,
  imports: [],
  templateUrl: './admin-report.component.html',
  styleUrl: './admin-report.component.scss'
})
export class AdminReportComponent {


  chartData: number[] = [1,2,3,4,5,6,7];
  chartLabels: string[] = ["1","2","3","4","5","6","7"];
  public chart: any;

  ngOnInit(): void {
    this.createChart();
  }

  createChart(){
    this.chart = new Chart("MyChart", {
      type: 'bar',
      // type: 'doughnut',
      data: {
        // labels: this.chartLabels, 
         labels: ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm","4pm","5pm" ],
	      //  datasets: [
        //   { label: "Ingresos:", data: this.chartData,},
        //   ]
        datasets: [{
          label: 'Ingresos',
          data: [12, 19, 3, 5, 2, 3, 6, 9, 12, 8],
          borderWidth: 1
        }]
      },
      options: { aspectRatio:3}
    });
  }

}
