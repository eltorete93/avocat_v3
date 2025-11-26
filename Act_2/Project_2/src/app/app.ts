import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrls: ['./app.css'],

})
export class App {

  constructor() {
    this.scrollTitle();
  }

  scrollTitle() {
    let msg = " Libreria Nexus  -  Cafeteria |  ";
    let pos = 0;

    const loop = () => {
      document.title = msg.substring(pos) + msg.substring(0, pos);
      pos = (pos + 1) % msg.length;
      setTimeout(loop, 300);
    };

    loop();
  }
}
