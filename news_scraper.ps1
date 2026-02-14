$url = "https://pa-pamekasan.go.id/"
$outputFile = "news_data.js"
$userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

try {
    $response = Invoke-WebRequest -Uri $url -UserAgent $userAgent -UseBasicParsing
    $html = $response.Content
    
    # regex for titles and links
    $newsItems = @()
    $count = 0
    
    $regex = '(?si)<h[2-4][^>]*?>\s*<a[^>]*?href="([^"]+?)"[^>]*?>(.*?)</a>\s*</h[2-4]>'
    $matches = [regex]::Matches($html, $regex)

    foreach ($match in $matches) {
        if ($count -ge 6) { break }
        
        $link = $match.Groups[1].Value
        # Ensure absolute link
        if ($link -notmatch '^http') {
            $link = "https://pa-pamekasan.go.id/" + $link.TrimStart('/')
        }

        $title = ($match.Groups[2].Value -replace '<.*?>', '').Trim()
        
        # Filter out non-news
        if ($link -match '/kategori/|/tag/|/search/|/feed/|/author/') { continue }
        if ($title.Length -lt 15) { continue }
        
        # Image search in context
        $pos = $match.Index
        $context = $html.Substring([math]::Max(0, $pos - 1000), [math]::Min(2000, $html.Length - [math]::Max(0, $pos - 1000)))
        $img = "assets/pa_pamekasan_official.jpg" # local fallback
        if ($context -match '(?i)<img.*?src=["''](https?://[^"'']+?\.(?:jpg|jpeg|png|gif|webp))["'']') {
            $img = $matches[1]
        }
        
        $newsItems += @{
            title = $title -replace '&nbsp;|&#\d+;', ' '
            link = $link
            description = "Klik detail untuk membaca berita selengkapnya dari website resmi Pengadilan Agama Pamekasan."
            image = $img
        }
        $count++
    }
    
    $jsonData = $newsItems | ConvertTo-Json -Depth 5
    # Wrap in JS variable assignment
    $jsContent = "const newsData = " + $jsonData + ";"
    $jsContent | Out-File -FilePath $outputFile -Encoding utf8
    Write-Host "Successfully extracted $count news items to $outputFile"
}
catch {
    Write-Error "Failed: $($_.Exception.Message)"
    if (-not (Test-Path $outputFile)) { "const newsData = [];" | Out-File -FilePath $outputFile }
}
