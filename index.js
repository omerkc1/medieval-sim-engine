import { createClient } from '@supabase/supabase-js'
import cron from 'node-cron'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
)

async function worldTick() {

  const { data: kingdoms } = await supabase
    .from('kingdoms')
    .select('*')

  for (let k of kingdoms) {

    let stabilityChange = Math.floor(Math.random() * 5 - 2)
    let wealthChange = Math.floor(Math.random() * 5 - 2)

    await supabase
      .from('kingdoms')
      .update({
        stability: k.stability + stabilityChange,
        wealth: k.wealth + wealthChange
      })
      .eq('id', k.id)
  }

  const { data: world } = await supabase
    .from('world_state')
    .select('*')
    .single()

  await supabase
    .from('world_state')
    .update({
      year: world.year + 1,
      global_tension: world.global_tension + Math.floor(Math.random() * 3)
    })
    .eq('id', 1)

  console.log("World advanced one year")
}

cron.schedule('*/20 * * * * *', worldTick)
