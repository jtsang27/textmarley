<template>
  <section id="contact" class="py-20 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="max-w-2xl mx-auto text-center">
        <h2 class="text-3xl font-bold mb-8">Ready to get started?</h2>
        <p class="text-gray-600 mb-8">
          Join thousands of businesses that trust TextMarley for their customer communication needs.
        </p>
        <form class="space-y-4" @submit.prevent="handleSubmit">
          <input
            type="email"
            v-model="email"
            placeholder="Enter your email"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
          />
          <button class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700">
            Start Free Trial
          </button>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')

const handleSubmit = () => {
  // Handle form submission
  console.log('Form submitted with email:', email.value)
}
</script>