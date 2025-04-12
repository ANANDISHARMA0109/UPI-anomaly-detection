# import shap
# import matplotlib.pyplot as plt
# from sklearn.preprocessing import StandardScaler
# from sklearn.neighbors import LocalOutlierFactor
# import pandas as pd

# def get_shap_plot(row):
#     # Create a small dummy dataset around the input row to satisfy LOF
#     df_sample = pd.DataFrame([row] * 6)  # make 6 copies to allow LOF n_neighbors=5
#     df_sample = df_sample[["amount"]]  # assuming only amount is numeric; else add more features

#     # Preprocess
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(df_sample)

#     # Fit LOF
#     model = LocalOutlierFactor(n_neighbors=2, novelty=True)
#     model.fit(X_scaled)

#     # SHAP Explanation
#     explainer = shap.Explainer(model.predict)
#     shap_values = explainer(X_scaled)

#     # Plot SHAP
#     fig, ax = plt.subplots()
#     shap.plots.waterfall(shap_values[0], show=True)
#     return fig


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neighbors import LocalOutlierFactor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def get_score_plot(row, df):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    from sklearn.preprocessing import StandardScaler

    # Convert timestamp and extract features
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()

    row['timestamp'] = pd.to_datetime(row['timestamp'])
    row['hour'] = row['timestamp'].hour
    row['day_of_week'] = row['timestamp'].day_name()

    # Add row to df temporarily for scaling
    df_temp = df.copy()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    # Filter numeric features
    features = ['amount', 'hour']
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df_temp[features])

    # Get standardized values for the last (new) row
    current_scaled = scaled[-1]

    # Prepare labels
    display_names = {
        'amount': f"Amount (₹{row['amount']})",
        'hour': f"Hour ({row['hour']})"
    }

    # Plot
    fig, ax = plt.subplots()
    sns.barplot(
        x=[display_names[f] for f in features],
        y=current_scaled,
        palette="coolwarm",
        ax=ax
    )
    ax.set_title("📊 Feature Deviation from User History")
    ax.set_ylabel("Z-score (Deviation from User's History)")
    ax.set_xlabel("Feature")

    for i, val in enumerate(current_scaled):
        ax.text(i, val, f"{val:.2f}", ha='center', va='bottom' if val > 0 else 'top')

    plt.tight_layout()
    return fig

