# 🔧 Troubleshooting

### Common Issues

#### Connection Errors

**Problem**: `Connection test failed`
**Solution**:
1. Verify your `IMMICH_BASE_URL` points to the root of your Immich instance (e.g., `https://your-immich-server.com`) and does not end with `/api`.
2. Check that your Immich server is accessible.
3. Ensure your API key is valid and has proper permissions.

```bash
# Test connectivity
curl -H "x-api-key: your-api-key" https://your-immich-server.com/server-info/ping
```

#### Authentication Errors

**Problem**: `401 Unauthorized`
**Solution**:
1. Verify your API key is correct
2. Check that the API key has sufficient permissions
3. Ensure the key hasn't expired

#### Rate Limiting

**Problem**: `429 Too Many Requests`
**Solution**:
1. Reduce request frequency
2. Increase rate limit settings in configuration
3. Implement exponential backoff

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python -m immich_mcp.server
```


### Performance Monitoring

Monitor server performance:

```bash
# Check memory usage
ps aux | grep immich-mcp

# Monitor logs
tail -f /var/log/immich-mcp.log
```

### Getting Help

If you encounter issues:

1. Check the [troubleshooting section](#troubleshooting)
2. Review [GitHub Issues](https://github.com/your-org/immich-mcp/issues)
3. Enable debug logging for detailed error information
4. Join our [Discord community](https://discord.gg/immich-mcp)
