# Incident and Rollback Drill

Scenario: version `v1.1.0` reduces memory below the application's working set. Pods become `OOMKilled`, restart, and fail the atomic Helm upgrade.

Investigate:

```powershell
kubectl get pods -n forgepulse-dev
kubectl describe pod -n forgepulse-dev <pod>
kubectl logs -n forgepulse-dev <pod> --previous
kubectl get events -n forgepulse-dev --sort-by=.lastTimestamp
helm history forgepulse -n forgepulse-dev
```

The `--atomic` deployment returns to the last healthy revision when readiness never succeeds. If manual rollback is needed:

```powershell
helm rollback forgepulse <healthy-revision> -n forgepulse-dev --wait
kubectl rollout status deployment/forgepulse -n forgepulse-dev
```

After recovery, fix resource values in Git, open a pull request, rerun the pipeline, and validate `/release` returns the expected Git SHA. Record timeline, impact, root cause, contributing controls, and prevention without blaming individuals.
