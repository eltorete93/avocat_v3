import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-cafe-nav',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './cafe-nav.html',
  styleUrls: ['./cafe-nav.css'],
})
export class CafeNav {}
