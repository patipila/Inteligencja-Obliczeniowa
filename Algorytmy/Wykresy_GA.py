import matplotlib.pyplot as plt
from sklearn.manifold import MDS

def plot_route_alternative(route, distance_matrix, title,save_path):
    # Zmiana wartości NaN na 0
    distance_matrix.fillna(0, inplace=True)

    # MDS - Multidimensional Scaling 
    mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42, normalized_stress='auto')
    coordinates = mds.fit_transform(distance_matrix)

    # Wykres
    plt.figure(figsize=(10, 8))
    plt.scatter(coordinates[:, 0], coordinates[:, 1], marker='o', label='Cities')

    # Dodanie numerów miast
    for i, txt in enumerate(range(len(coordinates))):
        plt.annotate(txt, (coordinates[i, 0], coordinates[i, 1]))

    # Narysowanie trasy
    for i in range(len(route) - 1):
        plt.plot([coordinates[route[i], 0], coordinates[route[i + 1], 0]],
                 [coordinates[route[i], 1], coordinates[route[i + 1], 1]], 'k-', alpha=0.7, linewidth=2, label='Route')

    # Podpisanie pierwszego i ostatniego miasta (po odwiedzeniu ostatniego miasta następuje powrót do pierwszego)
    plt.text(coordinates[route[0], 0], coordinates[route[0], 1], 'Start', fontsize=12, ha='right', color='green', weight='bold')
    plt.text(coordinates[route[-1], 0], coordinates[route[-1], 1], 'End', fontsize=12, ha='right', color='red', weight='bold')

    plt.title('Optimal Route Visualization'.format(title))
    plt.legend()
    plt.show()
    plt.savefig(save_path, bbox_inches='tight')


plot_route_alternative(route, distance_matrix, 'Example',"Wyniki_GA/Wykresy/.png")
