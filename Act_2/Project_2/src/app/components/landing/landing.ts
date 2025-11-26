import { Component } from '@angular/core';
import { NgxTypewriterComponent } from '@omnedia/ngx-typewriter';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [NgxTypewriterComponent],
  templateUrl: './landing.html',
  styleUrl: './landing.css',

})
export class Landing {

  Hero = {
    mainParraph:'Tu espacio para aprender,',
    secondParraph:'crear y disfrutar.',
    thirdParraph:'compartir y descubrir.',
    fourthParraph:'estudiar y soñar.',
    subtittle:'Librería universitaria, coworking y cafetería en un solo lugar.',
    button:'Descubrir más'
  }

}
