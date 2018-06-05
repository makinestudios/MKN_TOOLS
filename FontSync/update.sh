system=$(uname)
font_sync_fonts_directory=/Volumes/pegasus/00_LIBRARY/00_MKN_TOOLS/FontSync/MAkinE
if [[ $system == "Darwin" ]]
	then echo "SI";	local_font_dir=/Library/Fonts/MAkinE;
fi
if [[ $system == "Linux" ]]
	then echo "NO";	local_font_dir=/usr/share/fonts/MAkinE;
fi

echo $system 
echo $local_font_dir

if [[ -d $local_font_dir ]]
	then echo $local_font_dir "exists"; 
else
	mkdir local_font_dir;	
fi

echo 'Updating Local Fonts...'
rsync -rv --size-only  --include="*otf" --include="*OTF" --include="*ttf" --include="*TTF" --exclude="*" $font_sync_fonts_directory/ $local_font_dir/
echo 'Updating Local Fonts Permissons...'
#chmod 775 $local_font_dir/*
#chgrp editorial-graphics $local_font_dir/*
echo 'Updating Suppository Fonts...'
rsync -rv --size-only --include="*otf" --include="*OTF" --include="*ttf" --include="*TTF" --exclude="*"  $local_font_dir/ $font_sync_fonts_directory/
echo 'Done.'
