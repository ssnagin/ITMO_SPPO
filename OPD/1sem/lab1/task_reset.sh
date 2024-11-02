echo "I will try to erase lab0..."

cd ~

echo "Giving privledges"
chmod -R 777 lab0
echo "Removing ( -Rf Recursy + folder)"
rm -Rf lab0

echo "Done!"
