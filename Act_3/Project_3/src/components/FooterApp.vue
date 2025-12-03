<!-- Footer -->

<template>
  <footer class="bg-[#2c414f] text-white py-10 relative overflow-hidden">

    <div class="max-w-7xl mx-auto px-4 relative z-10">
      <div class="text-center space-y-4">

        <div class="flex items-center justify-center space-x-3">
          <img src="../assets/nexus_logo.png" alt="Nexus Logo" class="h-10 w-auto" />
            <h3 class="text-2xl font-semibold">{{ footerLinks.name }}</h3>
        </div>
          <p class="text-gray-300">{{  footerLinks.text }}</p>

        <!-- Social media -->
        <div class="flex justify-center space-x-6 mt-3">

          <a href="https://www.facebook.com/" target="_blank" rel="noopener noreferrer" class="hover:text-blue-700 transition">
            <Facebook class="w-7 h-7" />
          </a>

          <a href="https://www.instagram.com/" target="_blank" rel="noopener noreferrer" class="hover:text-rose-500 transition">
             <Instagram class="w-7 h-7" />
          </a>


          <a href="https://x.com/" target="_blank" rel="noopener noreferrer" class="hover:text-blue-500 transition">
             <Twitter class="w-7 h-7" />
          </a>


          <a href="https://www.whatsapp.com/?lang=en" target="_blank" rel="noopener noreferrer" class="hover:text-green-400 transition">
            <MessageCircle class="w-7 h-7" />
          </a>

        </div>

        <p class="text-gray-400 text-sm mt-6">{{ footerLinks.copyright }}</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { Facebook, Instagram, Twitter, MessageCircle } from "lucide-vue-next";

const footerLinks = {
  name: 'Nexus',
  text: 'Tu espacio para aprender, imaginar y disfrutar',
  copyright: '© 2025 Nexus. Todos los derechos reservados.'
}

</script>

<style scoped></style>
