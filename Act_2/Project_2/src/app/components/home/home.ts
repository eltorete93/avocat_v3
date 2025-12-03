import { Component } from '@angular/core';
import { Navbar } from '../navbar/navbar';
import { Landing } from '../landing/landing';
import { Testimonial } from '../testimonial/testimonial';
import { Footer } from '../footer/footer';
import { NewReleases } from '../new-releases/new-releases';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [Navbar, Landing, Testimonial,NewReleases ,Footer],
  templateUrl: './home.html',
  styleUrls: ['./home.css'],
})
export class Home {}
