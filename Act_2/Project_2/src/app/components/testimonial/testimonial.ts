import { Component, OnInit, OnDestroy, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-testimonial',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './testimonial.html',
  styleUrls: ['./testimonial.css'],
})
export class Testimonial implements OnInit, OnDestroy {
  current = 0;
  autoPlay = true;
  intervalMs = 5000;
  private autoTimer: any = null;

  /** Pause autoplay when user interacts */
  isPaused = false;

  testimonials = [
  {
  name: "Ava Thompson",
      handle: "@ava_thompson",
      review:
        "ScrollX UI is a game-changer! The animations are smooth, and the UI is beyond stunning.",
      avatar:
        "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=100&auto=format&fit=crop"
    },
    {
      name: "Elijah Carter",
      handle: "@elijah_ui",
      review:
        "Absolutely mesmerizing! The attention to detail in ScrollX UI is incredible.",
      avatar:
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=100&auto=format&fit=crop"
    },
    {
      name: "Sophia Martinez",
      handle: "@sophia_codes",
      review:
        "As a front-end developer, I love how intuitive and powerful ScrollX UI is. It's a must-have tool!",
      avatar:
        "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=100&auto=format&fit=crop"
    }

  ];

  ngOnInit(): void {
    this.startAuto();
  }

  ngOnDestroy(): void {
    this.stopAuto();
  }

  startAuto() {
    if (!this.autoPlay || this.autoTimer) return;
    this.autoTimer = setInterval(() => {
      if (!this.isPaused) this.next();
    }, this.intervalMs);
  }

  stopAuto() {
    if (this.autoTimer) {
      clearInterval(this.autoTimer);
      this.autoTimer = null;
    }
  }

  pause() { this.isPaused = true; }
  resume() { this.isPaused = false; }

  next() {
    this.current = (this.current + 1) % this.testimonials.length;
  }

  prev() {
    this.current = (this.current - 1 + this.testimonials.length) % this.testimonials.length;
  }

  goTo(i: number) {
    if (i >= 0 && i < this.testimonials.length) this.current = i;
  }

  @HostListener('window:keydown', ['$event'])
  onKey(ev: KeyboardEvent) {
    if (ev.key === 'ArrowLeft') this.prev();
    if (ev.key === 'ArrowRight') this.next();
  }

}
