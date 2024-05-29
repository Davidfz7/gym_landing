import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AvisosIndexComponent } from './avisos-index/avisos-index.component';

const routes: Routes = [
  { path:'avisos', component: AvisosIndexComponent},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AvisosRoutingModule { }
