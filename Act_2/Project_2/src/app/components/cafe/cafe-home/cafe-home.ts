import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CafeNav } from '../cafe-nav/cafe-nav';

@Component({
  selector: 'app-cafe-home',
  standalone: true,
  imports: [RouterLink, CafeNav],
  templateUrl: './cafe-home.html',
  styleUrls: ['./cafe-home.css'],
})
export class CafeHome {}
