import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../App.vue'

describe('App', () => {
  it('renders the default result message', () => {
    const wrapper = mount(App)

    expect(wrapper.text()).toContain(
      'Fill in your categories, weight them to 1.00, and the tally lands here.',
    )
  })

  it("adds a category when '+ new category' is clicked", async () => {
    const wrapper = mount(App)

    const initialCategories = wrapper.findAll('input[placeholder="Category name"]').length

    // Find the button with the exact text match from App.vue
    const addButton = wrapper
      .findAll('button')
      .find((btn) => btn.text().toLowerCase().includes('+ new category'))

    await addButton?.trigger('click')

    const updatedCategories = wrapper.findAll('input[placeholder="Category name"]').length

    expect(updatedCategories).toBe(initialCategories + 1)
  })

  it('updates the category name', async () => {
    const wrapper = mount(App)

    const input = wrapper.find('input[placeholder="Category name"]')

    await input.setValue('Assignments')

    expect((input.element as HTMLInputElement).value).toBe('Assignments')
  })

  it('adds an assessment', async () => {
    const wrapper = mount(App)

    const initialAssessments = wrapper.findAll('input[placeholder="Assessment name"]').length

    // App.vue uses "+ add entry" to append an assessment row
    const addEntryButton = wrapper
      .findAll('button')
      .find((btn) => btn.text().toLowerCase().includes('+ add entry'))

    await addEntryButton?.trigger('click')

    const updatedAssessments = wrapper.findAll('input[placeholder="Assessment name"]').length

    expect(updatedAssessments).toBe(initialAssessments + 1)
  })

  it('updates an assessment name', async () => {
    const wrapper = mount(App)

    const input = wrapper.find('input[placeholder="Assessment name"]')

    await input.setValue('Quiz 1')

    expect((input.element as HTMLInputElement).value).toBe('Quiz 1')
  })

  it('has a calculate button', () => {
    const wrapper = mount(App)

    expect(wrapper.text()).toContain('Calculate grade')
  })

  it('shows the total weight text', () => {
    const wrapper = mount(App)

    // App.vue prints "total weight 1.00" without a trailing colon
    expect(wrapper.text().toLowerCase()).toContain('total weight')
  })
})
