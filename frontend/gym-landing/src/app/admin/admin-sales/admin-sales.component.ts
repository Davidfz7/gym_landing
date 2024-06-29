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
import { MatTabChangeEvent } from '@angular/material/tabs';
import {MatIconModule} from '@angular/material/icon';
import { routes } from '../../app.routes';
import { RouterLink } from '@angular/router';


import Chart from 'chart.js/auto';

import { Subject, takeUntil } from 'rxjs';
import { GenericService } from '../../share/generic.service';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer } from '@angular/platform-browser';
import { AuthService } from '../../share/auth.service';

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

export interface datosSales {
  saleid: number;
  productid: number;
  quantity: number;
  date: string;
}

@Component({
  selector: 'app-admin-sales',
  standalone: true,
  imports: [
    MatFormFieldModule, MatInputModule, MatTableModule, MatSortModule, MatPaginatorModule, MatRippleModule, MatTabsModule, MatGridListModule, MatCardModule,
    ReactiveFormsModule,MatButtonModule,MatSelectModule, CommonModule,MatIconModule, RouterLink
  ],
  templateUrl: './admin-sales.component.html',
  styleUrl: './admin-sales.component.scss'
})
export class AdminSalesComponent {

  displayedColumns3: string[] = ['productid', 'quantity', 'date'];
  dataSource3: MatTableDataSource<datosSales>;


  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  datos:any;
  datosSales:any;
  destroy$:Subject<boolean>=new Subject<boolean>();
  dataProds:any;
  productDict:any;

  myForm2: FormGroup;

  dateNow: Date;
  dateString: string;
  imageUrl: any;
  logo:any;
  

  showPaginator = false;
  pageSize = 10;
  pageIndex = 0;
  


  constructor(private gService:GenericService,
    private router:Router,
    private route:ActivatedRoute,
    private httpClient:HttpClient,
    private sanitizer: DomSanitizer,
    private formBuilder: FormBuilder,
    private authService: AuthService,
  ) {


    this.listaProductos();
    this.listaSales();


  }

  ngOnInit(){

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
    this.gService.list('all-products/')
      .pipe(takeUntil(this.destroy$))
      .subscribe((data:any)=>{
        this.datos=data;
        console.log(this.datos);
        this.dataProds=this.datos;
      });
  }

  listaSales(){
    this.gService.list('all-sales/')
      .pipe(takeUntil(this.destroy$))
      .subscribe((data:any)=>{
        this.datosSales=data;
        console.log(this.datosSales);

        this.dataSource3 = new MatTableDataSource(this.datosSales);
        this.dataSource3.paginator = this.paginator;
        this.dataSource3.sort = this.sort;
  


      });
  }

  

  onSubmit() {
    
  }

  getCurrentFormattedDate(): string {
    const date = new Date();
    const year = date.getFullYear();
    const month = ('0' + (date.getMonth() + 1)).slice(-2); // Añade 1 porque los meses en JS son 0-indexed
    const day = ('0' + date.getDate()).slice(-2);
    console.log(`${year}-${month}-${day}`)
    return `${year}-${month}-${day}`;
  }

  stringToDate(dateString: string): Date {
    const [year, month, day] = dateString.split('-').map(Number);
    
    return new Date(year, month - 1, day); // Restamos 1 al mes porque los meses en JS son 0-indexed
  }

  onSubmitVenta() {
    if (this.myForm2.valid) {

      const formData = new FormData();

      // this.dateNow = this.stringToDate(this.getCurrentFormattedDate());
      this.dateString = this.getCurrentFormattedDate();
      // console.log(this.dateNow);

      formData.append('productid', this.myForm2.value.product);
      formData.append('quantity', this.myForm2.value.cantidad);
      formData.append('date', this.dateString);

      console.log(formData);
 

      this.gService.create('new-sale/', formData)
      .pipe(takeUntil(this.destroy$))
      .subscribe((data:any)=>{
        console.log(data);
        this.listaSales();
      });

  
    }
  }





  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource3.filter = filterValue.trim().toLowerCase();

    if (this.dataSource3.paginator) {
      this.dataSource3.paginator.firstPage();
    }

  }

}
