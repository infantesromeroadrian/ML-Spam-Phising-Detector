import { useEffect, useRef } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js';
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

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    cutout: '75%',
    plugins: {
      tooltip: { enabled: false },
      legend: { display: false },
    },
  };

  // Center text plugin
  useEffect(() => {
    const chart = chartRef.current;
    if (!chart) return;

    const plugin = {
      id: 'centerText',
      afterDraw: (chart: ChartJS) => {
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

    chart.options.plugins = {
      ...chart.options.plugins,
      centerText: plugin as any,
    };
    chart.update();
  }, [value, color]);

  return (
    <div className="relative">
      <Doughnut ref={chartRef} data={data} options={options} />
      <div className="text-center mt-2">
        <p className="text-sm text-gray-400 uppercase tracking-wide">{label}</p>
      </div>
    </div>
  );
};
