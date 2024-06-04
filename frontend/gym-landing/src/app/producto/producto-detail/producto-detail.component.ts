import {MatCardModule} from '@angular/material/card';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GenericService } from '../../share/generic.service';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { DomSanitizer } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { Subject, takeUntil } from 'rxjs';
import { forkJoin } from 'rxjs';
import { RouterLink } from '@angular/router';
import {
  CarouselComponent,
  CarouselControlComponent,
  CarouselIndicatorsComponent,
  CarouselInnerComponent,
  CarouselItemComponent,
  ThemeDirective
} from '@coreui/angular';
import { NgFor } from '@angular/common';
import { provideAnimations } from '@angular/platform-browser/animations';
import { AlertModule } from '@coreui/angular';
import { environment } from '../../environments/environment';
import {MatButtonModule} from '@angular/material/button';
import {MatDividerModule} from '@angular/material/divider';
import {MatIconModule} from '@angular/material/icon';



@Component({
  selector: 'app-producto-detail',
  standalone: true,
  imports: [MatCardModule, CommonModule, ThemeDirective, CarouselComponent, CarouselIndicatorsComponent, 
    CarouselInnerComponent, NgFor, CarouselItemComponent, CarouselControlComponent, RouterLink, AlertModule,MatButtonModule,
    MatDividerModule, MatIconModule],
  providers: [
    provideAnimations()],
  templateUrl: './producto-detail.component.html',
  styleUrl: './producto-detail.component.scss'
})
export class ProductoDetailComponent implements OnInit {
  product: any;
  productImages: any[];
  productId: any;

  datos:any;
  destroy$:Subject<boolean>=new Subject<boolean>();

  datosImgs: any;
  datosComb:any;
  baseUrl: string = environment.apiURL;



  constructor(private gService:GenericService,
    private router:Router,
    private route:ActivatedRoute,
    private httpClient:HttpClient,
    private sanitizer: DomSanitizer
    ){

      // this.listaProductos();
      // this.listaImagenes();
    }

  ngOnInit(): void {
    const productId = this.route.snapshot.paramMap.get('id');
    this.loadProductDetails(productId);
    
  }

  loadProductDetails(productId: string): void {
    forkJoin([
      this.gService.list(`get-product/${productId}/`),
      this.gService.list('get-imgs-names/')
    ]).subscribe(([productData, imageData]: [any, any[]]) => {
      this.product = productData;
      const imageDataForProduct = imageData.find(image => image.id === +productId);

      if (imageDataForProduct) {
        this.productImages = imageDataForProduct.imgs_list.map(img => `${this.baseUrl}${this.product.pimgspath}${img}`);
      }
    });
  }




  
  // listaProductos(){
  //   this.productId = this.route.snapshot.paramMap.get('id');
  //   this.gService.list(`get-product/${this.productId}/`)
  //     .pipe(takeUntil(this.destroy$))
  //     .subscribe((data:any)=>{
  //       this.product = data;
  //       console.log(this.product);
  //       // this.filteredProducts = data;
  //     });
  // }

  // listaImagenes(){
  //   this.gService.list('get-imgs-names/')
  //     .pipe(takeUntil(this.destroy$))
  //     .subscribe((data:any)=>{
  //       const imageData = data.find(image => image.id === +this.productId);
  //       if (imageData) {
  //         this.productImages = imageData.imgs_list.map(img => `${this.baseUrl}${this.product.pimgspath}${img}`);
  //       }
  //       console.log("datos:" );
  //       console.log(this.datosComb);
  //     });
  // }
}
