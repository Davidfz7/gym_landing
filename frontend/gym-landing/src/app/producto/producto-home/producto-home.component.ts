import { Component } from '@angular/core';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatIconModule} from '@angular/material/icon';
import {FormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatDividerModule} from '@angular/material/divider';
import {MatSliderModule} from '@angular/material/slider';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatMenuModule} from '@angular/material/menu';
import { RouterLink } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';
import { GenericService } from '../../share/generic.service';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { DomSanitizer } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { environment } from '../../environments/environment';
import {Breakpoints} from '@angular/cdk/layout';

@Component({
  selector: 'app-producto-home',
  standalone: true,
  imports: [MatGridListModule, MatCardModule, MatButtonModule, MatFormFieldModule, MatInputModule, FormsModule, MatButtonModule, MatIconModule,MatDividerModule,
    MatCheckboxModule,
    MatSliderModule,
    MatMenuModule,
    RouterLink, 
    CommonModule,
  ],
  templateUrl: './producto-home.component.html',
  styleUrl: './producto-home.component.scss'
})
export class ProductoHomeComponent  {
  filteredProducts = [];  // Lista filtrada de productos
  searchValue: string = '';

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
      this.listaProductos();
      
    }

    listaProductos(){
      this.gService.list('get-all-products/')
        .pipe(takeUntil(this.destroy$))
        .subscribe((data:any)=>{
          this.datos=data;
          console.log(this.datos);
          // this.filteredProducts = data;
          this.listaImagenes();
        });
    }
  
    viewProduct(productId: number) {
      this.router.navigate(['/product', productId]);
    }

    listaImagenes(){
      this.gService.list('get-imgs-names/')
        .pipe(takeUntil(this.destroy$))
        .subscribe((data:any)=>{
          this.datosImgs=data;
          console.log(this.datosImgs);
  
          this.datosComb = this.datos.map(product => {
            const imageData = this.datosImgs.find(image => image.id === product.id);
            if (imageData) {
              console.log(product);
              return {
                ...product,
                imgUrl: imageData.imgs_list.length ? `${this.baseUrl}${product.pimgspath}${imageData.imgs_list[0]}` : null
              };
            }
            return product;
          });
          console.log("datos:" );
          console.log(this.datosComb);
        });
    }

  
}
