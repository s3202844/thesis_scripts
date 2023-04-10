description=$1
folder_path=$2
features="disp ela_distr ela_level ela_meta ic nbc pca"

if [ ! -d "$description" ]; then
    mkdir $description
fi

for id in {1..5}
do
    for feature in $features
    do
        python scripts/atom_process.py -d=$description -p=$folder_path -f=$feature -i=$id &
        sleep 1
        echo $id $feature
    done
done
