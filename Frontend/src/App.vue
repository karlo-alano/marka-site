<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import 'primeicons/primeicons.css'

interface Assessment {
  name: string
  earned_points: number
  total_points: number
}

interface GradeCategory {
  category: string
  weight: number
  assessments: Assessment[]
}

interface BreakdownItem {
  category: string
  percentage: number
  weight: number
  contribution: number
}

const API_URL = 'https://marka-api.karloalano.site/calculate'

const categories = reactive<GradeCategory[]>([
  {
    category: 'Quizzes',
    weight: 0.3,
    assessments: [{ name: 'Quiz 1', earned_points: 0, total_points: 0 }],
  },
  {
    category: 'Exams',
    weight: 0.7,
    assessments: [{ name: 'Midterm', earned_points: 0, total_points: 0 }],
  },
])

const subjectGrade = ref<number | null>(null)
const breakdown = ref<BreakdownItem[]>([])
const errorMsg = ref('')
const loading = ref(false)

function addCategory() {
  categories.push({
    category: 'New category',
    weight: 0,
    assessments: [{ name: 'Assessment 1', earned_points: 0, total_points: 0 }],
  })
}

function removeCategory(index: number) {
  categories.splice(index, 1)
}

function addAssessment(catIndex: number) {
  const category = categories[catIndex]
  if (!category) return

  category.assessments.push({
    name: `Assessment ${category.assessments.length + 1}`,
    earned_points: 0,
    total_points: 0,
  })
}

function removeAssessment(catIndex: number, assIndex: number) {
  const category = categories[catIndex]
  if (!category) return
  category.assessments.splice(assIndex, 1)
}

const totalWeight = computed(() => categories.reduce((sum, c) => sum + (Number(c.weight) || 0), 0))

const weightIsBalanced = computed(() => Math.abs(totalWeight.value - 1) < 0.005)

// letter mark for the stamp, purely cosmetic flavor on top of the numeric grade
function letterFor(grade: number) {
  if (grade >= 96.7) return '1.00'
  if (grade >= 93.4) return '1.25'
  if (grade >= 90.1) return '1.50'
  if (grade >= 86.7) return '1.75'
  if (grade >= 83.4) return '2.00'
  if (grade >= 80.1) return '2.25'
  if (grade >= 76.7) return '2.50'
  if (grade >= 73.4) return '2.75'
  if (grade >= 70.0) return '3.00'
  if (grade >= 50) return '4.00/INC'
  return 'F'
}

async function calculate() {
  errorMsg.value = ''
  subjectGrade.value = null
  breakdown.value = []
  loading.value = true

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ categories }),
    })

    if (!res.ok) {
      throw new Error(`Server responded with ${res.status}`)
    }

    const data = await res.json()
    subjectGrade.value = data.subject_grade
    breakdown.value = data.breakdown
  } catch (err) {
    errorMsg.value =
      err instanceof Error
        ? `Couldn't reach the backend: ${err.message}`
        : 'Something went wrong calculating your grade.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="min-h-screen w-screen bg-custom-purple px-6 py-12 md:px-14 lg:px-20 overflow-y-auto">
    <!-- masthead -->
    <header class="max-w-6xl mx-auto mb-12 flex items-end justify-between gap-6 flex-wrap">
      <div>
        <div class="flex items-baseline gap-3">
          <h1 class="font-serif text-5xl md:text-6xl text-custom-tan tracking-tight">Marka</h1>
          <span class="font-mono text-xs uppercase tracking-[0.3em] text-custom-lime/80">
            grade ledger
          </span>
        </div>
        <p class="mt-2 text-custom-tan/60 font-serif italic text-lg">
          Every quiz and exam, tallied to one number.
        </p>
      </div>
      <div class="font-mono text-xs text-custom-tan/40 text-right leading-relaxed">
        <div>RECORD&nbsp;NO. {{ new Date().getFullYear() }}–01</div>
        <div>
          {{ categories.length }} categor{{ categories.length === 1 ? 'y' : 'ies' }} on file
        </div>
      </div>
    </header>

    <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-10 items-start">
      <!-- ledger entries -->
      <div class="space-y-8">
        <section v-for="(cat, catIndex) in categories" :key="catIndex" class="group">
          <!-- category header row -->
          <div class="flex items-center gap-4 pb-3 border-b-2 border-custom-tan/30">
            <span class="font-mono text-custom-lime text-sm w-6 shrink-0">
              {{ String(catIndex + 1).padStart(2, '0') }}
            </span>
            <input
              v-model="cat.category"
              class="flex-1 bg-transparent font-serif text-2xl text-custom-tan border-none outline-none placeholder:text-custom-tan/30"
              placeholder="Category name"
            />
            <label
              class="flex items-center gap-2 font-mono text-xs text-custom-tan/50 uppercase tracking-wider"
            >
              weight
              <input
                v-model.number="cat.weight"
                type="number"
                step="0.01"
                min="0"
                max="1"
                class="w-16 bg-transparent border-b border-custom-tan/30 focus:border-custom-lime text-custom-tan text-sm font-mono outline-none text-right pb-0.5 transition-colors"
              />
            </label>
            <button
              @click="removeCategory(catIndex)"
              class="text-custom-tan/30 hover:text-custom-lime transition-colors cursor-pointer opacity-0 group-hover:opacity-100"
              title="Remove category"
            >
              <i class="pi pi-trash text-sm"></i>
            </button>
          </div>

          <!-- assessment rows -->
          <div class="divide-y divide-custom-tan/10">
            <div
              v-for="(ass, assIndex) in cat.assessments"
              :key="assIndex"
              class="flex items-center gap-3 py-2.5"
            >
              <input
                v-model="ass.name"
                class="flex-1 bg-transparent text-custom-tan/90 text-sm outline-none placeholder:text-custom-tan/30 font-medium"
                placeholder="Assessment name"
              />
              <div class="flex items-center gap-1.5 font-mono text-sm">
                <input
                  v-model.number="ass.earned_points"
                  type="number"
                  class="w-14 bg-custom-purple border border-custom-tan/20 focus:border-custom-lime rounded px-2 py-1 text-custom-tan text-right outline-none transition-colors"
                />
                <span class="text-custom-tan/30">/</span>
                <input
                  v-model.number="ass.total_points"
                  type="number"
                  class="w-14 bg-custom-purple border border-custom-tan/20 focus:border-custom-lime rounded px-2 py-1 text-custom-tan text-right outline-none transition-colors"
                />
              </div>
              <button
                @click="removeAssessment(catIndex, assIndex)"
                class="text-custom-tan/20 hover:text-custom-lime transition-colors cursor-pointer"
                title="Remove assessment"
              >
                <i class="pi pi-times text-xs"></i>
              </button>
            </div>
          </div>

          <button
            @click="addAssessment(catIndex)"
            class="mt-3 font-mono text-xs uppercase tracking-wider text-custom-mint hover:text-custom-lime transition-colors cursor-pointer"
          >
            + add entry
          </button>
        </section>

        <!-- footer controls -->
        <div class="pt-4 flex items-center gap-5 flex-wrap">
          <button
            @click="addCategory"
            class="border border-custom-tan/30 hover:border-custom-lime hover:text-custom-lime text-custom-tan font-mono text-xs uppercase tracking-wider px-4 py-2.5 rounded-full transition-colors cursor-pointer"
          >
            + new category
          </button>

          <span
            class="font-mono text-xs uppercase tracking-wider"
            :class="weightIsBalanced ? 'text-custom-lime' : 'text-custom-tan/40'"
          >
            total weight {{ totalWeight.toFixed(2) }}
            <span v-if="!weightIsBalanced">&middot; should equal 1.00</span>
          </span>
        </div>

        <button
          @click="calculate"
          :disabled="loading"
          class="bg-custom-lime text-custom-purple font-serif font-bold text-lg px-8 py-3.5 rounded-full shadow-[0_4px_0_0_rgba(0,0,0,0.15)] hover:-translate-y-0.5 hover:shadow-[0_6px_0_0_rgba(0,0,0,0.15)] active:translate-y-0 active:shadow-[0_2px_0_0_rgba(0,0,0,0.15)] transition-all disabled:opacity-50 disabled:translate-y-0 disabled:shadow-none cursor-pointer"
        >
          {{ loading ? 'Tallying…' : 'Calculate grade' }}
        </button>

        <p v-if="errorMsg" class="font-mono text-sm text-rose-300">{{ errorMsg }}</p>
      </div>

      <!-- result: the stamp -->
      <aside class="sticky top-10 bg-custom-tan rounded-3xl p-7 shadow-2xl">
        <div class="font-mono text-[11px] uppercase tracking-[0.25em] text-custom-purple/50 mb-5">
          Final mark
        </div>

        <div v-if="subjectGrade !== null" class="space-y-6">
          <div class="relative flex flex-col items-center py-4">
            <div
              class="w-36 h-36 rounded-full border-[3px] border-custom-purple flex flex-col items-center justify-center -rotate-3"
            >
              <span class="font-serif text-5xl font-bold text-custom-purple leading-none">
                {{ subjectGrade }}
              </span>
              <span class="font-mono text-[10px] text-custom-purple/50 mt-1">percent</span>
            </div>
            <div
              class="absolute -right-1 top-0 bg-custom-purple text-custom-lime font-mono text-sm font-bold w-10 h-10 rounded-full flex items-center justify-center rotate-12"
            >
              {{ letterFor(subjectGrade) }}
            </div>
          </div>

          <div class="space-y-2.5">
            <div
              v-for="item in breakdown"
              :key="item.category"
              class="flex items-center justify-between text-sm border-b border-custom-purple/10 pb-2"
            >
              <div>
                <div class="text-custom-purple font-semibold">{{ item.category }}</div>
                <div class="font-mono text-[11px] text-custom-purple/40">
                  weight {{ item.weight }} &middot; earns {{ item.contribution }}
                </div>
              </div>
              <div class="font-mono text-custom-purple font-bold">{{ item.percentage }}%</div>
            </div>
          </div>
        </div>

        <div v-else class="text-custom-purple/50 text-sm font-serif italic leading-relaxed py-6">
          Fill in your categories, weight them to 1.00, and the tally lands here.
        </div>
      </aside>
    </div>
  </main>
</template>

<style scoped>
input[type='number']::-webkit-inner-spin-button,
input[type='number']::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type='number'] {
  -moz-appearance: textfield;
}
</style>
