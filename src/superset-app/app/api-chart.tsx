import { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import type { ChartData, ChartOptions } from 'chart.js/auto';

const APIChart: React.FC = () => {
  const [chartData, setChartData] = useState<ChartData<'bar'>>();

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.post('http://your-superset-domain/api/v1/chart/data', {
        // Your API query configuration
      }, {
        headers: {
          Authorization: `Bearer your-api-token`,
        },
      });

      const data = response.data.result[0].data;
      
      // Transform the data to match Chart.js format
      const transformedData: ChartData<'bar'> = {
        labels: data.map((item: any) => item.label), // Adjust according to your data structure
        datasets: [
          {
            label: 'Your Data Label',
            data: data.map((item: any) => item.value), // Adjust according to your data structure
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
          },
        ],
      };

      setChartData(transformedData);
    };

    fetchData();
  }, []);

  const options: ChartOptions<'bar'> = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div>
      {chartData && (
        <Bar data={chartData} options={options} />
      )}
    </div>
  );
};

export default APIChart;
