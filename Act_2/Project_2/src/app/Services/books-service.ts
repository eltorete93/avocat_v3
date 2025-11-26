import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book } from '../components/books/books';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class BooksService {
  private apiUrl = '/Act_2/Project_2/public/prueba.json';


  constructor(private http: HttpClient) {}

  getUpcomingBooks(): Observable<Book[]> {
    return this.http.get<Book[]>(this.apiUrl);
  }
}
