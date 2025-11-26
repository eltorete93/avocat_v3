import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-cafe-about',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cafe-about.html',
  styleUrls: ['./cafe-about.css'],
})
export class CafeAbout {
  team = [
    {
      name: 'María García',
      role: 'Head Barista',
      image: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=300'
    },
    {
      name: 'Carlos Ruiz',
      role: 'Pastry Chef',
      image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300'
    },
    {
      name: 'Ana López',
      role: 'Manager',
      image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=300'
    }
  ];
}
