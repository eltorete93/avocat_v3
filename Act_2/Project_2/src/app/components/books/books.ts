import { Component } from '@angular/core';

export interface Book {
  id?: number;
  title: string;
  author: string;
  image: string;
  releaseDate: string;
  price?: number;
  description?: string;
  category?: string;
}

@Component({
  selector: 'app-books',
  standalone: true,
  imports: [],
  templateUrl:'./books.html',
  styleUrls: ['./books.css']
})
export class Books {}
