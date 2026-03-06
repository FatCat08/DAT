import ReactECharts from 'echarts-for-react';
import { BarChart3, Maximize2, Download } from 'lucide-react';
import './style.css';
import { useMemo } from 'react';

interface ChartPanelProps {
    chartConfig: any;
    chartData: any;
}

export default function ChartPanel({ chartConfig, chartData }: ChartPanelProps) {
    const option = useMemo(() => {
        if (!chartConfig || chartConfig.chartType === 'none' || !chartData?.rows) {
            return null;
        }

        const type = chartConfig.chartType;
        const columns = chartData.columns || [];
        const rows = chartData.rows || [];

        // Simple helper to find index of a column
        const getColIdx = (colName: string) => columns.indexOf(colName);

        let seriesData: any[] = [];
        let xAxisData: any[] = [];

        if (type === 'pie') {
            const nameIdx = getColIdx(chartConfig.nameColumn);
            const valIdx = getColIdx(chartConfig.valueColumn);
            if (nameIdx >= 0 && valIdx >= 0) {
                seriesData = rows.map((r: any[]) => ({ name: r[nameIdx], value: r[valIdx] }));
            }
        } else {
            const xIdx = getColIdx(chartConfig.xAxis);
            const yIdx = getColIdx(chartConfig.yAxis);
            if (xIdx >= 0 && yIdx >= 0) {
                xAxisData = rows.map((r: any[]) => r[xIdx]);
                seriesData = rows.map((r: any[]) => r[yIdx]);
            }
        }

        const baseOption: any = {
            backgroundColor: 'transparent',
            tooltip: {
                trigger: type === 'pie' ? 'item' : 'axis',
                backgroundColor: 'rgba(17, 24, 39, 0.9)',
                borderColor: '#374151',
                textStyle: { color: '#F9FAFB' }
            },
            grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
            title: {
                text: chartConfig.title || '',
                textStyle: { color: '#F3F4F6', fontSize: 14 }
            }
        };

        if (type === 'pie') {
            baseOption.series = [{
                type: 'pie',
                radius: '50%',
                data: seriesData,
                emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
            }];
        } else {
            baseOption.xAxis = {
                type: 'category',
                data: xAxisData,
                axisLine: { lineStyle: { color: '#374151' } },
                axisLabel: { color: '#9CA3AF' }
            };
            baseOption.yAxis = {
                type: 'value',
                splitLine: { lineStyle: { color: '#374151', type: 'dashed' } },
                axisLabel: { color: '#9CA3AF' }
            };
            baseOption.series = [{
                name: chartConfig.yAxis || 'Value',
                type: type,
                data: seriesData,
                itemStyle: { color: '#3B82F6', borderRadius: type === 'bar' ? [4, 4, 0, 0] : 0 }
            }];
        }

        return baseOption;
    }, [chartConfig, chartData]);

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
                {option ? (
                    <div className="chart-card">
                        <div className="card-header">
                            <h3>{chartConfig?.title || 'Chart Rendering'}</h3>
                            <span className="badge success">Live</span>
                        </div>
                        <div className="card-body">
                            <ReactECharts
                                option={option}
                                style={{ height: '350px', width: '100%' }}
                                opts={{ renderer: 'svg' }}
                            />
                        </div>
                    </div>
                ) : (
                    <div className="empty-chart">
                        <div className="placeholder-text">Ask a question that involves numeric data to see a chart.</div>
                    </div>
                )}
            </div>
        </div>
    );
}
