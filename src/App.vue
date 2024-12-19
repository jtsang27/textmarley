<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-50 to-white">
    <Navigation />
    <Hero />
    <Features />
    <Pricing />
    <Contact />
    <Footer />
  </div>
</template>

<script setup>
import Navigation from './components/Navigation.vue'
import Hero from './components/Hero.vue'
import Features from './components/Features.vue'
import Pricing from './components/Pricing.vue'
import Contact from './components/Contact.vue'
import Footer from './components/Footer.vue'
</script>

<style>
body {
  font-family: 'Inter', sans-serif;
}
</style>