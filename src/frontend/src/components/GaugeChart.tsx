import { useEffect, useRef } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Plugin } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip);

interface GaugeChartProps {
  value: number; // 0-100
  label: string;
  color: string;
}

export const GaugeChart = ({ value, label, color }: GaugeChartProps) => {
  const chartRef = useRef<ChartJS<'doughnut'>>(null);

  const data = {
    datasets: [
      {
        data: [value, 100 - value],
        backgroundColor: [color, '#1f2937'],
        borderWidth: 0,
        circumference: 180,
        rotation: 270,
      },
    ],
  };

  const centerTextPlugin: Plugin<'doughnut'> = {
    id: 'centerText',
    afterDraw: (chart) => {
      const { ctx, chartArea } = chart;
      if (!chartArea) return;

      const centerX = (chartArea.left + chartArea.right) / 2;
      const centerY = (chartArea.top + chartArea.bottom) / 2 + 20;

      ctx.save();
      ctx.font = 'bold 2rem sans-serif';
      ctx.fillStyle = color;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`${value.toFixed(1)}%`, centerX, centerY);
      ctx.restore();
    },
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    cutout: '75%',
    plugins: {
      tooltip: { enabled: false },
      legend: { display: false },
    },
  };

  return (
    <div className="relative">
      <Doughnut ref={chartRef} data={data} options={options} plugins={[centerTextPlugin]} />
      <div className="text-center mt-2">
        <p className="text-sm text-gray-400 uppercase tracking-wide">{label}</p>
      </div>
    </div>
  );
};
