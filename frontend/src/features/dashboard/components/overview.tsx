import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from 'recharts'

const data = [
  {
    name: 'Jan',
    uploads: 234,
  },
  {
    name: 'Feb',
    uploads: 278,
  },
  {
    name: 'Mar',
    uploads: 312,
  },
  {
    name: 'Apr',
    uploads: 289,
  },
  {
    name: 'May',
    uploads: 456,
  },
  {
    name: 'Jun',
    uploads: 387,
  },
  {
    name: 'Jul',
    uploads: 356,
  },
  {
    name: 'Aug',
    uploads: 290,
  },
  {
    name: 'Sep',
    uploads: 345,
  },
  {
    name: 'Oct',
    uploads: 478,
  },
  {
    name: 'Nov',
    uploads: 389,
  },
  {
    name: 'Dec',
    uploads: 425,
  },
]

export function Overview() {
  return (
    <ResponsiveContainer width='100%' height={350}>
      <BarChart data={data}>
        <XAxis
          dataKey='name'
          stroke='#888888'
          fontSize={12}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          stroke='#888888'
          fontSize={12}
          tickLine={false}
          axisLine={false}
          tickFormatter={(value) => `${value}`}
        />
        <Bar
          dataKey='uploads'
          fill='currentColor'
          radius={[4, 4, 0, 0]}
          className='fill-primary'
        />
      </BarChart>
    </ResponsiveContainer>
  )
}
