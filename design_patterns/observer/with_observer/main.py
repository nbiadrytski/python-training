from design_patterns.observer.with_observer.kpis import KPIs
from design_patterns.observer.with_observer.currentkpis import CurrentKPIs
from design_patterns.observer.with_observer.forecastkpis import ForecastKPIs


# Report on current KPI values
with KPIs() as kpis:
    with CurrentKPIs(kpis), ForecastKPIs(kpis):
        kpis.set_kpis(25, 10, 5)
        kpis.set_kpis(100, 50, 30)
        kpis.set_kpis(50, 10, 20)

print ('\n***Exited context managers.***\n\n')
kpis.set_kpis(150, 110, 120)