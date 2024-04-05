import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProductoIndexComponent } from './producto-index/producto-index.component';

const routes: Routes = [
  { path:'productos', component: ProductoIndexComponent},

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProductoRoutingModule { }
