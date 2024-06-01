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
import {MatButtonModule} from '@angular/material/button';
import {MatSelectModule} from '@angular/material/select';
import { FormGroup, ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';

import Chart from 'chart.js/auto';

import { Subject, takeUntil } from 'rxjs';
import { GenericService } from '../../share/generic.service';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { DomSanitizer } from '@angular/platform-browser';

export interface ProdsData {
  id: number;
  pname: string;
  pbrand: string;
  pdescription: string;
  pstatus: string;
  pcategory: string;
  pprice: string;
  pstock: number;
  pimgspath:string;
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
    ReactiveFormsModule,MatButtonModule,MatSelectModule, HttpClientModule,CommonModule,
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
  datosSales:any;
  destroy$:Subject<boolean>=new Subject<boolean>();
  dataProds:any;


  chartData: number[] = [1,2,3,4,5,6,7];
  chartLabels: string[] = ["1","2","3","4","5","6","7"];
  public chart: any;
  public chart2: any;

  myForm: FormGroup;
  myForm2: FormGroup;

  imageUrl: any;
  logo:any;
  multipleImages:any;
  imagesArray:any;


  constructor(private gService:GenericService,
    private router:Router,
    private route:ActivatedRoute,
    private httpClient:HttpClient,
    private sanitizer: DomSanitizer,
    private formBuilder: FormBuilder
  ) {


    this.listaProductos();
    this.listaSales();
  }

  ngOnInit(){
    this.createChart();
    this.myForm = this.formBuilder.group({
      pname: ['', Validators.required],
      pbrand: ['', Validators.required],
      pdescription: ['', Validators.required],
      pstatus: ['', Validators.required],
      pcategory: ['', Validators.required],
      pprice:['', Validators.required],
      pstock:['', Validators.required],
    });

    this.myForm2 = this.formBuilder.group({
      product: ['', Validators.required],
      cantidad: [1, [Validators.required, Validators.min(1)]]
    });

    
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

  listaSales(){
    this.gService.list('get-all-sales/')
      .pipe(takeUntil(this.destroy$))
      .subscribe((data:any)=>{
        this.datosSales=data;
        console.log(this.datosSales);
      });
  }

  onSubmit() {
    if (this.myForm.valid) {
      // this.myForm.value.pimgspath=this.logo;
      const formData = new FormData();
      // const formData = this.myForm.value;
      formData.append('pname', this.myForm.value.pname);
      formData.append('pbrand', this.myForm.value.pbrand);
      formData.append('pdescription', this.myForm.value.pdescription);
      formData.append('pstatus', this.myForm.value.pstatus);
      formData.append('pcategory', this.myForm.value.pcategory);
      formData.append('pprice', this.myForm.value.pprice);
      formData.append('pstock', this.myForm.value.pstock);
      // formData.append('pimgspath', this.multipleImages);

      for (let i = 0; i < this.multipleImages.length; i++) {
        formData.append('pimgspath', this.multipleImages[i]);
      }
  
      console.log(formData);
      // const formData = this.myForm.value;
      this.gService.create('add-new-product/', formData)
      .pipe(takeUntil(this.destroy$))
      .subscribe((data:any)=>{
        console.log(data);
        this.listaProductos();
      });

  
    }
  }


  uploadMultiple(event: any) {
    const filesList: FileList = event.target.files;
  
    // Convert FileList to array of file objects
    this.multipleImages = Array.from(filesList);
    this.imagesArray = [];
  
    // Convert FileList to array
    const filesArray = Array.from(this.multipleImages);
  
    filesArray.forEach((element: Blob) => {
      if (element) {
        const reader = new FileReader();
        reader.readAsDataURL(element);
        reader.onload = () => {
          this.imagesArray.push(reader.result);
        };
      }
    });
  }

  // onMultipleSubmit(id:any){
  //   if(this.multipleImages.length > 0){
  //     const formData = new FormData();
  //     for(let img of this.multipleImages){
  //       formData.append('files', img);
  //     }
  //     this.httpClient.post<any>(`http://localhost:3000/multiplefiles/${id}`, formData).subscribe(
  //       (res) => console.log(res),
  //       (err) => console.log(err)
  //     );
  //   }
  // }


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

