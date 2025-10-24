import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Header } from './header/header';
import{ LandingCarousel } from './landing-carousel/landing-carousel';
import { BookCatalog } from './book-catalog/book-catalog';
import { Footer } from './footer/footer';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Header, LandingCarousel, BookCatalog, Footer],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {

}
