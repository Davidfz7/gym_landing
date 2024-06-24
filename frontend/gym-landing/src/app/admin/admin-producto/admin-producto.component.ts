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
  selector: 'app-admin-producto',
  standalone: true,
  imports: [
    MatFormFieldModule, MatInputModule, MatTableModule, MatSortModule, MatPaginatorModule, MatRippleModule, MatTabsModule, MatGridListModule, MatCardModule,
    ReactiveFormsModule,MatButtonModule,MatSelectModule, CommonModule,MatIconModule, RouterLink
  ],
  templateUrl: './admin-producto.component.html',
  styleUrl: './admin-producto.component.scss'
})
export class AdminProductoComponent implements AfterViewInit {

  displayedColumns: string[] = ['pname', 'pdescription', 'pstatus', 'pprice', 'pstock'];
  dataSource: MatTableDataSource<ProdsData>;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  datos:any;
  datosSales:any;
  destroy$:Subject<boolean>=new Subject<boolean>();
  dataProds:any;
  productDict:any;



  myForm: FormGroup;
  myForm2: FormGroup;

  dateNow: Date;
  dateString: string;
  imageUrl: any;
  logo:any;
  multipleImages:any;
  imagesArray:any;

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



  }

  ngOnInit(){

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

  calculosData(){

  }




  

 

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

}
