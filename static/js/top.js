var day_id={{day.id}};
        var alltags=[{% for tag in alltags %}"{{tag.name}}"{% if loop.last %}{% else %},{% endif %}{% endfor %}];
        var allpeople=[{% for person in allpeople %}"{{person}}"{% if loop.last %}{% else %},{% endif %}{% endfor %}];
        var recenttags=[{% for tag in recenttags %}"{{tag.name}}"{% if loop.last %}{% else %},{% endif %}{% endfor %}];
        var exipeople=[{% for pdf in persondays %}"{{pdf.person}}"{% if loop.last %}{% else %},{% endif %}{% endfor %}];
        var exitags=[{% for tag in exitags %}"{{tag.name}}"{% if loop.last %}{% else %},{% endif %}{% endfor %}];