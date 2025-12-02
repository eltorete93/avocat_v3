<template>
  <footer class="bg-[#2c414f] text-white py-10 relative overflow-hidden">

    <!-- Líneas animadas -->
    <div class="absolute inset-0">
      <div class="animate-line w-full h-0.5 bg-white/5 absolute top-10"></div>
      <div class="animate-line w-full h-0.5 bg-white/5 absolute top-20"></div>
      <div class="animate-line w-full h-0.5 bg-white/5 absolute top-32"></div>
    </div>

    <div class="max-w-7xl mx-auto px-4 relative z-10">
      <div class="text-center space-y-4">
        <h3 class="text-2xl font-semibold">Nexus</h3>
        <p class="text-gray-300">Tu espacio para aprender, imaginar y disfrutar</p>

        <!-- Redes -->
        <div class="flex justify-center space-x-6 mt-3">

          <a href="#" class="hover:text-blue-700 transition">
            <Facebook class="w-7 h-7" />
          </a>

          <a href="#" class="hover:text-rose-500 transition">
             <Instagram class="w-7 h-7" />
          </a>


          <a href="#" class="hover:text-blue-500 transition">
             <Twitter class="w-7 h-7" />
          </a>


          <a href="https://wa.me/0000000000" class="hover:text-green-400 transition">
            <MessageCircle class="w-7 h-7" />
          </a>

        </div>

        <p class="text-gray-400 text-sm mt-6">© 2025 Nexus. Todos los derechos reservados.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { Facebook, Instagram, Twitter, MessageCircle } from "lucide-vue-next";
</script>

<style>
@keyframes movingLine {
  0% { transform: translateX(-100%); opacity: 0.3; }
  100% { transform: translateX(100%); opacity: 0.6; }
}

.animate-line {
  animation: movingLine 8s linear infinite;
}
</style>
