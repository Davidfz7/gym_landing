import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProductoIndexComponent } from './producto-index/producto-index.component';
import { ProductoPesasComponent } from './producto-pesas/producto-pesas.component';
import { ProductoEquiposComponent } from './producto-equipos/producto-equipos.component';
import { ProductoMaquinasComponent } from './producto-maquinas/producto-maquinas.component';
import { ProductoDetailComponent } from './producto-detail/producto-detail.component';
import { ProductoHomeComponent } from './producto-home/producto-home.component';

const routes: Routes = [
  { path:'productos', component: ProductoIndexComponent},
  { path:'productos/home', component: ProductoHomeComponent},
  { path:'productos/pesas', component: ProductoPesasComponent},
  { path:'productos/equipos', component: ProductoEquiposComponent},
  { path:'productos/maquinas', component: ProductoMaquinasComponent},
  { path:'product/:id', component: ProductoDetailComponent }

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProductoRoutingModule { }
