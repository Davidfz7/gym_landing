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

@Component({
  selector: 'app-producto-index',
  standalone: true,
  imports: [MatGridListModule, MatCardModule, MatButtonModule, MatFormFieldModule, MatInputModule, FormsModule, MatButtonModule, MatIconModule,MatDividerModule,
    MatCheckboxModule,
    MatSliderModule,
    MatMenuModule,
    RouterLink, 
    CommonModule,
  ],
  templateUrl: './producto-index.component.html',
  styleUrl: './producto-index.component.scss'
})
export class ProductoIndexComponent {
  value = '';
  max = 5000000;
  min = 0;
  step = 50000;
  thumbLabel = false;
  value2 = 0;

  datos:any;
  destroy$:Subject<boolean>=new Subject<boolean>();

  datosImgs: any;
  datosComb:any;
  baseUrl: string = 'http://127.0.0.1:8000';

  constructor(private gService:GenericService,
    private router:Router,
    private route:ActivatedRoute,
    private httpClient:HttpClient,
    private sanitizer: DomSanitizer
    ){
      this.listaProductos();
      this.listaImagenes();
    }

  ngOnInit(): void {
    
  }

  listaProductos(){
    this.gService.list('get-all-products/')
      .pipe(takeUntil(this.destroy$))
      .subscribe((data:any)=>{
        this.datos=data;
        console.log(this.datos);
      });
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
