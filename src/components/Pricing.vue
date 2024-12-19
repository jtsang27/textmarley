<template>
  <section id="pricing" class="py-20 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 class="text-3xl font-bold text-center mb-12">Simple, Transparent Pricing</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <PricingCard
          v-for="plan in plans"
          :key="plan.name"
          v-bind="plan"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import PricingCard from './PricingCard.vue'

const plans = [
  {
    name: 'Starter',
    price: 29,
    features: ['1,000 messages/month', 'Basic analytics', '1 team member'],
    isPopular: false
  },
  {
    name: 'Professional',
    price: 99,
    features: ['10,000 messages/month', 'Advanced analytics', '5 team members'],
    isPopular: true
  },
  {
    name: 'Enterprise',
    price: null,
    priceLabel: 'Custom',
    features: ['Unlimited messages', 'Custom analytics', 'Unlimited team members'],
    isPopular: false
  }
]
</script>