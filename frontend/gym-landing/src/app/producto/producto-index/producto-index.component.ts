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

@Component({
  selector: 'app-producto-index',
  standalone: true,
  imports: [MatGridListModule, MatCardModule, MatButtonModule, MatFormFieldModule, MatInputModule, FormsModule, MatButtonModule, MatIconModule,MatDividerModule,
    MatCheckboxModule,
    MatSliderModule,
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

}
