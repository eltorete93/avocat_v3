import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LandingCarousel } from './landing-carousel';

describe('LandingCarousel', () => {
  let component: LandingCarousel;
  let fixture: ComponentFixture<LandingCarousel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LandingCarousel]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LandingCarousel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
