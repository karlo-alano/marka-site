<script setup lang="ts">
import { ref, reactive } from 'vue'
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

const API_URL = 'http://localhost:8000/calculate'

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
    category: 'New Category',
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

const totalWeight = () => categories.reduce((sum, c) => sum + (Number(c.weight) || 0), 0)

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
  <main class="h-screen w-screen bg-custom-purple p-10 overflow-y-auto">
    <div class="text-4xl font-extrabold text-custom-tan">Marka</div>
    <div class="text-custom-tan/70 mb-8">Your grades, weighted and tallied</div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Categories input -->
      <div class="lg:col-span-2 space-y-5">
        <div
          v-for="(cat, catIndex) in categories"
          :key="catIndex"
          class="bg-custom-tan rounded-2xl p-5 shadow-lg border-2"
        >
          <div class="flex items-center gap-3 mb-4">
            <input
              v-model="cat.category"
              class="flex-1 bg-transparent text-custom-purple font-bold text-lg border-b-2 border-custom-purple/30 focus:border-custom-purple outline-none pb-1"
              placeholder="Category name"
            />
            <div class="flex items-center gap-2">
              <span class="text-custom-purple/70 text-sm">Weight</span>
              <input
                v-model.number="cat.weight"
                type="number"
                step="0.01"
                min="0"
                max="1"
                class="w-20 bg-white/60 rounded-lg px-2 py-1 text-custom-purple text-sm outline-none"
              />
            </div>
            <button
              @click="removeCategory(catIndex)"
              class="text-custom-purple/50 hover:text-red-600 font-bold px-2 cursor-pointer"
              title="Remove category"
            >
              <i class="pi pi-trash"></i>
            </button>
          </div>

          <div class="space-y-2">
            <div
              v-for="(ass, assIndex) in cat.assessments"
              :key="assIndex"
              class="flex items-center gap-2 bg-white/50 rounded-xl px-3 py-2"
            >
              <input
                v-model="ass.name"
                class="flex-1 bg-transparent text-custom-purple text-sm outline-none"
                placeholder="Assessment name"
              />
              <input
                v-model.number="ass.earned_points"
                type="number"
                class="w-20 bg-white/70 rounded-lg px-2 py-1 text-custom-purple text-sm outline-none text-right"
                placeholder="earned"
              />
              <span class="text-custom-purple/50">/</span>
              <input
                v-model.number="ass.total_points"
                type="number"
                class="w-20 bg-white/70 rounded-lg px-2 py-1 text-custom-purple text-sm outline-none text-right"
                placeholder="total"
              />
              <button
                @click="removeAssessment(catIndex, assIndex)"
                class="text-custom-purple/40 hover:text-red-600 px-1 cursor-pointer"
                title="Remove assessment"
              >
                <i class="pi pi-trash"></i>
              </button>
            </div>
          </div>

          <button
            @click="addAssessment(catIndex)"
            class="mt-3 text-custom-purple font-semibold text-sm hover:underline cursor-pointer"
          >
            + Add Activity
          </button>
        </div>

        <div class="flex items-center gap-4">
          <button
            @click="addCategory"
            class="bg-custom-mint text-custom-purple font-bold px-4 py-2 rounded-xl hover:opacity-90 transition cursor-pointer w-50 hover:-translate-y-1"
          >
            + Add Category
          </button>
          <span
            class="text-sm"
            :class="totalWeight() === 1 ? 'text-custom-lime' : 'text-custom-tan/70'"
          >
            total weight: {{ totalWeight().toFixed(2) }}
            <span v-if="totalWeight() !== 1">(should be 1.00)</span>
          </span>
        </div>

        <button
          @click="calculate"
          :disabled="loading"
          class="bg-custom-tan text-custom-purple font-extrabold px-6 py-3 rounded-xl shadow-md hover:opacity-90 transition disabled:opacity-50 w-50 cursor-pointer mt-10"
        >
          {{ loading ? 'Calculating…' : 'Calculate grade' }}
        </button>

        <div v-if="errorMsg" class="text-red-300 font-medium">{{ errorMsg }}</div>
      </div>

      <!-- Result panel -->
      <div class="bg-custom-mint rounded-2xl p-6 shadow-lg h-fit sticky top-10 border-2">
        <div class="text-custom-purple font-bold text-lg mb-4">Result</div>

        <div v-if="subjectGrade !== null" class="space-y-4">
          <div class="text-5xl font-extrabold text-custom-purple">{{ subjectGrade }}%</div>

          <div class="space-y-2 mt-4">
            <div
              v-for="item in breakdown"
              :key="item.category"
              class="bg-custom-tan/60 rounded-lg p-3"
            >
              <div class="flex justify-between text-custom-purple font-semibold text-sm">
                <span>{{ item.category }}</span>
                <span>{{ item.percentage }}%</span>
              </div>
              <div class="flex justify-between text-custom-purple/70 text-xs mt-1">
                <span>weight {{ item.weight }}</span>
                <span>contributes {{ item.contribution }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-custom-purple/60 text-sm">
          fill in your categories and hit calculate to see your grade here.
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped></style>
