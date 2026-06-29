import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../App.vue'

describe('App', () => {
  it('renders the default result message', () => {
    const wrapper = mount(App)

    expect(wrapper.text()).toContain(
      'fill in your categories and hit calculate to see your grade here.',
    )
  })

  it("adds a category when '+ Add Category' is clicked", async () => {
    const wrapper = mount(App)

    const initialCategories = wrapper.findAll('input[placeholder="Category name"]').length

    await wrapper
      .findAll('button')
      .find((btn) => btn.text().includes('+ Add Category'))
      ?.trigger('click')

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

    await wrapper
      .findAll('button')
      .find((btn) => btn.text().includes('+ Add Activity'))
      ?.trigger('click')

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

    expect(wrapper.text()).toContain('total weight:')
  })
})
