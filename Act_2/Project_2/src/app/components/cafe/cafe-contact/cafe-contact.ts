import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-cafe-contact',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './cafe-contact.html',
  styleUrls: ['./cafe-contact.css'],
})
export class CafeContact implements OnInit {
  contactForm!: FormGroup;
  submitted = false;
  formSuccess = false;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.contactForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      message: ['', [Validators.required, Validators.minLength(10)]]
    });
  }

  get f() {
    return this.contactForm.controls;
  }

  onSubmit(): void {
    this.submitted = true;

    if (this.contactForm.invalid) {
      return;
    }

    // Simulate form submission
    console.log('Form submitted:', this.contactForm.value);
    this.formSuccess = true;

    // Reset form after 3 seconds
    setTimeout(() => {
      this.contactForm.reset();
      this.submitted = false;
      this.formSuccess = false;
    }, 3000);
  }
}
