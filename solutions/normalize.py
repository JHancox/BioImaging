# TODO Add a new transform to the Compose input list
trans = Compose([LoadImaged(keys="image"), EnsureChannelFirstd(keys="image", channel_dim=-1), NormalizeIntensityd(keys="image"),])

#Create the data iterator and dataset
data_iterator = iter(data_list)
dataset = IterableDataset(data=data_iterator, transform=trans)

# Load the data
dataloader = DataLoader(dataset=dataset, batch_size=3, num_workers=2)

# retrieve the first batch
d = first(dataloader)

img = np.array(d["image"][0])
# TODO - Remember that MatplotLib expects channels last - use numpy to do this
img = np.moveaxis(img, 0, -1)
plt.figure(figsize=(5,5))
plt.imshow(img)
plt.title('Nomalized Image')
plt.show()