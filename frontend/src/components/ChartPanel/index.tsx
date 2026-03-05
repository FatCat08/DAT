import ReactECharts from 'echarts-for-react';
import { BarChart3, Maximize2, Download } from 'lucide-react';
import './style.css';

export default function ChartPanel() {
    // Placeholder mock option for the EChart to prove it renders
    const option = {
        backgroundColor: 'transparent',
        tooltip: {
            trigger: 'axis',
            backgroundColor: 'rgba(17, 24, 39, 0.9)',
            borderColor: '#374151',
            textStyle: { color: '#F9FAFB' }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '10%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: ['Oct', 'Nov', 'Dec'],
            axisLine: { lineStyle: { color: '#374151' } },
            axisLabel: { color: '#9CA3AF' }
        },
        yAxis: {
            type: 'value',
            splitLine: { lineStyle: { color: '#374151', type: 'dashed' } },
            axisLabel: { color: '#9CA3AF' }
        },
        series: [
            {
                name: 'Sales ($)',
                type: 'bar',
                barWidth: '40%',
                itemStyle: {
                    color: '#3B82F6',
                    borderRadius: [4, 4, 0, 0]
                },
                data: [12000, 15000, 24000]
            }
        ]
    };

    return (
        <div className="chart-panel">
            <div className="chart-header">
                <h2 className="panel-title">
                    <BarChart3 size={18} className="title-icon" />
                    <span>Data Visualization</span>
                </h2>
                <div className="chart-actions">
                    <button className="tool-btn"><Download size={16} /></button>
                    <button className="tool-btn"><Maximize2 size={16} /></button>
                </div>
            </div>

            <div className="chart-content">
                <div className="chart-card">
                    <div className="card-header">
                        <h3>Q4 Sales Breakdown (Mock)</h3>
                        <span className="badge success">+24% MoM</span>
                    </div>
                    <div className="card-body">
                        <ReactECharts
                            option={option}
                            style={{ height: '350px', width: '100%' }}
                            opts={{ renderer: 'svg' }}
                        />
                    </div>
                    <div className="card-footer">
                        <p>Dataset: <code>sales_records_2025.db</code></p>
                    </div>
                </div>
            </div>
        </div>
    );
}
