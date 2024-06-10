for file in *; do
    if [[ -f $file ]]; then
        sed -i 's/\r//g' $file
    fi 
done
