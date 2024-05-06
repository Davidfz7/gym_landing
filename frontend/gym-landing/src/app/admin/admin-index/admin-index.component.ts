import {AfterViewInit, Component, ViewChild} from '@angular/core';
import {MatPaginator, MatPaginatorModule} from '@angular/material/paginator';
import {MatSort, MatSortModule} from '@angular/material/sort';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatRippleModule} from '@angular/material/core';
import {MatTabsModule} from '@angular/material/tabs';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatCardModule} from '@angular/material/card';
import { FormGroup, ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';

import Chart from 'chart.js/auto';

import { Subject, takeUntil } from 'rxjs';
import { GenericService } from '../../share/generic.service';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { DomSanitizer } from '@angular/platform-browser';

export interface ProdsData {
  pname: string;
  pdescription: string;
  pstatus: string;
  pprice: string;
  pstock: number;
  // pimgspath:string;
}

export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
}

const ELEMENT_DATA: PeriodicElement[] = [
  {position: 1, name: 'Hydrogen', weight: 1.0079},
  {position: 2, name: 'Helium', weight: 4.0026},
  {position: 3, name: 'Lithium', weight: 6.941},
  // {position: 4, name: 'Beryllium', weight: 9.0122},
  // {position: 5, name: 'Boron', weight: 10.811},
];


@Component({
  selector: 'app-admin-index',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, MatTableModule, MatSortModule, MatPaginatorModule, MatRippleModule, MatTabsModule, MatGridListModule, MatCardModule,
    ReactiveFormsModule,
  ],
  templateUrl: './admin-index.component.html',
  styleUrl: './admin-index.component.scss'
})
export class AdminIndexComponent implements AfterViewInit {
  
  displayedColumns: string[] = ['pname', 'pdescription', 'pstatus', 'pprice', 'pstock'];
  dataSource: MatTableDataSource<ProdsData>;

  displayedColumns2: string[] = ['position', 'name', 'weight'];
  dataSource2 = ELEMENT_DATA;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  datos:any;
  destroy$:Subject<boolean>=new Subject<boolean>();
  dataProds:any;


  chartData: number[] = [1,2,3,4,5,6,7];
  chartLabels: string[] = ["1","2","3","4","5","6","7"];
  public chart: any;
  public chart2: any;

  myForm: FormGroup;


  constructor(private gService:GenericService,
    private router:Router,
    private route:ActivatedRoute,
    private httpClient:HttpClient,
    private sanitizer: DomSanitizer) {

    
    

    this.listaProductos();
  }

  ngOnInit(): void {
    this.createChart();
  }

 

  ngAfterViewInit() {
    
  }

  ngAfterContentInit(){
    
  }

  listaProductos(){
    this.gService.list('get-all-products/')
      .pipe(takeUntil(this.destroy$))
      .subscribe((data:any)=>{
        this.datos=data;
        console.log(this.datos);
        this.dataProds=this.datos;
        this.dataSource = new MatTableDataSource(this.dataProds);
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
      });
  }

  createChart(){
  
    this.chart = new Chart("MyChart", {
      type: 'bar', //this denotes tha type of chart

      data: {// values on X-Axis
        labels: ['2022-05-10', '2022-05-11', '2022-05-12','2022-05-13',
								 '2022-05-14', '2022-05-15', '2022-05-16','2022-05-17', ], 
	       datasets: [
          {
            label: "Sales",
            data: ['467','576', '572', '79', '92',
								 '574', '573', '576'],
                 borderWidth: 1,
            backgroundColor: '#D6A328'
          },
          {
            label: "Profit",
            data: ['542', '542', '536', '327', '17',
									 '0.00', '538', '541'],
                   borderWidth: 1,
            backgroundColor: '#FBF791',
          }  
        ]
      },
      options: {
        aspectRatio:3.0
      }
      
    });

    this.chart2 = new Chart("MyChart2", {
      // type: 'bar',
      type: 'pie',
      data: {
        // labels: this.chartLabels, 
         labels: ["8am", "9am", "10am", "11am", "12pm"],
	      //  datasets: [
        //   { label: "Ingresos:", data: this.chartData,},
        //   ]
        datasets: [{
          label: 'Ingresos',
          data: [12, 19, 3, 5, 2],
          borderWidth: 1
        }]
      },
      options: { aspectRatio:3}
    });
    
  }

  

  

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }
}

