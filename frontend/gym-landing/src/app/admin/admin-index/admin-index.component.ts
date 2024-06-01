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

  dataSource2: MatTableDataSource<any>;
  displayedColumns2: string[] = ['position', 'name', 'quantity']; // Ajusta las columnas que deseas mostrar


  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  datos:any;
  datosSales:any;
  destroy$:Subject<boolean>=new Subject<boolean>();
  dataProds:any;
  productDict:any;


  chartData: number[] = [1,2,3,4,5,6,7];
  chartLabels: string[] = ["1","2","3","4","5","6","7"];
  chartProductNames: string[] = [];
  chartRevenue: number[] = [];
  public chart: any;
  public chart2: any;

  doughnutChartLabels: string[] = [];
  doughnutChartData: number[] = [];

  myForm: FormGroup;
  myForm2: FormGroup;

  dateNow: Date;
  dateString: string;
  imageUrl: any;
  logo:any;
  multipleImages:any;
  imagesArray:any;
  


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

        this.prepareChartData();
        this.prepareDoughnutChartData();
        this.createChart();

        
  
        this.loadSoldProds();

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
 

      this.gService.create('add-new-sale/', formData)
      .pipe(takeUntil(this.destroy$))
      .subscribe((data:any)=>{
        console.log(data);
        this.listaSales();
      });

  
    }
  }

  loadSoldProds(){
    const productDict = this.dataProds.reduce((dict, product) => {
      dict[product.id] = product;
      return dict;
    }, {});

      // Agrupar las ventas por producto y calcular la cantidad total vendida
      const salesByProduct = this.datosSales.reduce((acc, sale) => {
        if (!acc[sale.productid]) {
          acc[sale.productid] = {
            productid: sale.productid,
            quantity: 0
          };
        }
        acc[sale.productid].quantity += sale.quantity;
        return acc;
      }, {});

      // Convertir a un array de objetos { productid, quantity }
      const productsByQuantity = Object.keys(salesByProduct).map(productId => ({
        productid: productId,
        quantity: salesByProduct[productId].quantity
      }));

      // Ordenar por cantidad vendida en orden descendente
      productsByQuantity.sort((a, b) => b.quantity - a.quantity);

      // Seleccionar los primeros 5 productos (los más vendidos)
      const top5Products = productsByQuantity.slice(0, 3);

      // Mapear los datos para la tabla
      
       // Mapear los datos para la tabla
       const tableData = top5Products.map((product, index) => ({
        position: index + 1,
        name: productDict[product.productid]?.pname || 'Unknown Product',
        quantity: product.quantity
      }));

      // Asignar los datos al dataSource
      this.dataSource2 = new MatTableDataSource(tableData);

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


  prepareChartData() {
    // Crear un diccionario de productos para una búsqueda rápida
  const productDict = this.dataProds.reduce((dict, product) => {
    dict[product.id] = product;
    return dict;
  }, {});

  // Agrupar las ventas por mes y calcular los ingresos
  const salesByMonth = this.datosSales.reduce((acc, sale) => {
    const month = sale.date.slice(0, 7); // Obtener el año y mes en formato "YYYY-MM"
    if (!acc[month]) {
      acc[month] = { quantity: 0, revenue: 0 };
    }
    acc[month].quantity += sale.quantity;
    acc[month].revenue += sale.quantity * productDict[sale.productid].pprice;
    return acc;
  }, {});

  // Ordenar las claves de los meses y limitar a los últimos 6 meses
  const sortedMonths = Object.keys(salesByMonth)
    .sort((a, b) => new Date(a).getTime() - new Date(b).getTime())
    .slice(-6); // Obtener los últimos 6 meses

  // Preparar los datos para Chart.js
  this.chartLabels = sortedMonths;
  this.chartData = sortedMonths.map(month => salesByMonth[month].quantity);
  this.chartRevenue = sortedMonths.map(month => salesByMonth[month].revenue);
  }

  prepareDoughnutChartData() {
    // Crear un diccionario de productos para una búsqueda rápida
    const productDict = this.dataProds.reduce((dict, product) => {
      dict[product.id] = product;
      return dict;
    }, {});

    // Agrupar las ventas por producto y calcular los ingresos totales
    const salesByProduct = this.datosSales.reduce((acc, sale) => {
      if (!acc[sale.productid]) {
        acc[sale.productid] = 0;
      }
      acc[sale.productid] += sale.quantity * productDict[sale.productid].pprice; // Multiplicar la cantidad vendida por el precio del producto
      return acc;
    }, {});

    // Convertir a un array de objetos { productid, earnings }
    const productsWithEarnings = Object.keys(salesByProduct).map(productId => ({
      productid: productId,
      earnings: salesByProduct[productId]
    }));

    productsWithEarnings.sort((a, b) => b.earnings - a.earnings);
    const top8Products = productsWithEarnings.slice(0, 8);

       // Obtener los nombres de los productos y los ingresos totales para los top 8
       this.doughnutChartLabels = top8Products.map(product => productDict[product.productid].pname);
       this.doughnutChartData = top8Products.map(product => product.earnings);
  }

  createChart(){
  
    this.chart = new Chart("MyChart", {
      type: 'bar',
      data: {
        labels: this.chartLabels,
        datasets: [
          {
            label: 'Ventas',
            data: this.chartData,
            borderWidth: 1,
            backgroundColor: '#D6A328',
            yAxisID: 'y-axis-sales'
          },
          {
            label: 'Ingresos',
            data: this.chartRevenue,
            borderWidth: 1,
            backgroundColor: '#FBF791',
            yAxisID: 'y-axis-revenue'
          }
        ]
      },
      options: {
        aspectRatio: 3.0,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Mes'
            }
          },
          'y-axis-sales': {
            type: 'linear',
            position: 'left',
            title: {
              display: true,
              text: 'Cantidad de Ventas'
            }
          },
          'y-axis-revenue': {
            type: 'linear',
            position: 'right',
            title: {
              display: true,
              text: 'Ingresos'
            },
            grid: {
              drawOnChartArea: false // Sólo dibuja la cuadrícula para el eje de ventas
            }
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              title: (context) => {
                return `Mes: ${context[0].label}`;
              },
              label: (context) => {
                const dataset = context.dataset.label;
                const value = context.raw;
                return `${dataset}: ${value}`;
              }
            }
          }
        }
      }
    });

    this.chart2 = new Chart("MyChart2", {
      // // type: 'bar',
      // type: 'pie',
      // data: {
      //   // labels: this.chartLabels, 
      //    labels: ["8am", "9am", "10am", "11am", "12pm"],
	    //   //  datasets: [
      //   //   { label: "Ingresos:", data: this.chartData,},
      //   //   ]
      //   datasets: [{
      //     label: 'Ingresos',
      //     data: [12, 19, 3, 5, 2],
      //     borderWidth: 1
      //   }]
      // },
      // options: { aspectRatio:3}
      
      type: 'pie',
      data: {
        labels: this.doughnutChartLabels,
        datasets: [{
          label: 'Ganancias por Producto',
          data: this.doughnutChartData,
          // backgroundColor: [
          //   '#FF6384',
          //   '#36A2EB',
          //   '#FFCE56',
          //   '#4BC0C0',
          //   '#9966FF',
          //   '#FF9F40',
          //   '#FF6384',
          //   '#36A2EB'
          // ]
        }]
      },
      options: {
        aspectRatio: 3,
        plugins: {
          tooltip: {
            callbacks: {
              label: (tooltipItem) => {
                let label = tooltipItem.label || '';
                if (label) {
                  label += ': ';
                }
                const value = tooltipItem.raw || 0;
                return `${label}₡${Number(value).toFixed(2)}`; // Formatear el valor como dinero
              }
            }
          }
        }
      }
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

